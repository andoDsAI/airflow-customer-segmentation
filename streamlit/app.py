import os
import sys

import numpy as np
import pandas as pd
import pandas_profiling
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from streamlit_pandas_profiling import st_profile_report

import streamlit as st

repo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")

sys.path.insert(0, repo_path)
from utils.helpers import get_data_from_db, load_pkl


def get_data(config):
    df = get_data_from_db(query=f"SELECT * FROM {config.TABLE_NAME}", out_type="df")
    # df = pd.read_csv("src/data/mall_customers.csv", encoding="unicode_escape")
    # df.rename(mapper=config.COLUMN_MAPPING, axis=1, inplace=True)
    return df


def get_model(customer_type: str, algorithm: str):
    model = load_pkl(f"{repo_path}/models/{customer_type}_{algorithm}.pkl")
    return model


def pre_process(df, config, customer_type):
    """Get data to predict

    Args:
        df (pd.DataFrame): DataFrame to pre-process
        config (_type_): config of the customer type
        customer_type (_type_): customer type
    """
    # drop the columns that are not needed
    training_columns = config.TRAINING_COLUMNS
    df.drop(columns=[col for col in df.columns if col not in training_columns], inplace=True)

    # convert the categorical columns to numerical columns
    categorical_columns = config.CATEGORICAL_COLUMNS
    for col in categorical_columns:
        # fill missing value with most frequent value
        df[col].fillna(df[col].mode()[0], inplace=True)
        label_encoder = load_pkl(f"{repo_path}/models/{customer_type}_{col}_label_encoder.pkl")
        df[col] = label_encoder.transform(df[col])

    numeric_columns = [col for col in training_columns if col not in categorical_columns]
    # fill missing value with 0
    for col in numeric_columns:
        df[col].fillna(0, inplace=True)

    scaler = load_pkl(f"{repo_path}/models/{customer_type}_scaler.pkl")
    df = scaler.transform(df)
    return df


def main():
    st.set_page_config(
        page_title="Customer Segmentation",
        page_icon="🦈",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    st.title("Customer Segmentation")
    # get customer type
    customer_type = st.selectbox("Select a customer type", ["", "mall", "e_commerce"])
    show_eda = st.checkbox("Show Exploratory Data Analysis", value=False)
    if customer_type == "":
        return

    # get config
    exec(f"from configs import {customer_type.lower()}_config")
    config = eval(f"{customer_type.lower()}_config")
    # get data
    data = get_data(config=config)

    if show_eda:
        # eda with pandas profiling
        st.subheader("Exploratory Data Analysis")
        pr = pandas_profiling.ProfileReport(data)
        st_profile_report(pr)

    list_algo = [""] + list(config.MODEL_CONFIG.keys())
    algorithm = st.selectbox("Select a clustering algorithm", list_algo)
    if algorithm == "":
        return

    # get model
    model = get_model(customer_type=customer_type, algorithm=algorithm)
    # prediction
    data = pre_process(df=data, config=config, customer_type=customer_type)
    labels = model.predict(data)

    # dimensionality reduction
    if data.shape[1] > 2:
        pca = PCA(n_components=2)
        data = pca.fit_transform(data)

    data_plot = pd.DataFrame({"x": data[:, 0], "y": data[:, 1], "label": labels})

    # plot cluster scatter with plotly
    st.subheader("Customer Segmentation clustering")
    # random color code with number of clusters for visualization
    num_clusters = len(list(set(labels)))
    colors = ["#%06X" % np.random.randint(0, 0xFFFFFF) for _ in range(num_clusters)]
    data_plot["color"] = data_plot["label"].apply(lambda x: colors[x])
    fig = px.scatter(
        data_plot,
        x="x",
        y="y",
        color="color",
        hover_name="label",
        template="ggplot2",
    )
    # hide grid and axis
    fig.update_layout(
        showlegend=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
    )
    st.plotly_chart(fig)

    # plot cluster distribution with seaborn
    st.subheader("Clustering distribution")
    fig = px.histogram(
        data_plot,
        x="label",
        category_orders=dict(label=sorted(list(set(labels)))),
        nbins=5,
        template="seaborn",
    )
    # hide grid and axis
    fig.update_layout(bargap=0.3, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
