import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import sys

repo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")

sys.path.insert(0, repo_path)
from utils.helpers import load_pkl, get_data_from_db

st.title("Customer Segmentation")
st.subheader("Customer Segmentation using K-Means Clustering")


def get_data(config):
    data = get_data_from_db(
        query=f"SELECT * FROM {config.TABLE_NAME}", 
        out_type="df"
    )
    return data


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
    customer_type = st.selectbox("Select a customer type", ["mall", "e_commerce"])
    algorithm = st.selectbox("Select a clustering algorithm", ["k_means", "gaussian_mixture"])
    # get option selection
    exec(f"from configs import {customer_type.lower()}_config")
    config = eval(f"{customer_type.lower()}_config")
    
    model = get_model(customer_type=customer_type, algorithm=algorithm)
    data = get_data(config=config)
    data = pre_process(df=data, config=config, customer_type=customer_type)
    
    # predict
    y = model.predict(data)
    
    # plot cluster distribution
    plt.figure(figsize=(10, 5))
    plt.title("Cluster Distribution")
    plt.xlabel("Cluster")
    plt.ylabel("Count")
    plt.hist(y, bins=len(np.unique(y)))
    st.pyplot()
    

if __name__ == "__main__":
    main()
