import argparse
import os

import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tqdm import tqdm

from utils.helpers import get_data_from_db, save_pkl


def pre_processing(df: pd.DataFrame, args) -> pd.DataFrame:
    """Pre-process the data to training model

    Args:
        df (pd.DataFrame): DataFrame to pre-process

    Returns:
        pd.DataFrame: Pre-processed DataFrame
    """
    # drop the columns that are not needed
    training_columns = config.TRAINING_COLUMNS
    df.drop(columns=[col for col in df.columns if col not in training_columns], inplace=True)

    current_path = os.path.dirname(os.path.abspath(__file__))
    # convert the categorical columns to numerical columns
    categorical_columns = config.CATEGORICAL_COLUMNS
    for col in categorical_columns:
        # fill missing value with most frequent value
        df[col].fillna(df[col].mode()[0], inplace=True)
        label_encoder = LabelEncoder()
        df[col] = label_encoder.fit_transform(df[col])
        save_path = os.path.join(
            current_path, "models", f"{args.customer_type}_{col}_label_encoder.pkl"
        )
        save_pkl(data=label_encoder, file_path=save_path)

    numeric_columns = [col for col in training_columns if col not in categorical_columns]
    # fill missing value with 0
    for col in numeric_columns:
        df[col].fillna(0, inplace=True)

    # scale the data
    scaler = StandardScaler()
    df = scaler.fit_transform(df)
    save_path = os.path.join(current_path, "models", f"{args.customer_type}_scaler.pkl")
    save_pkl(data=scaler, file_path=save_path)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_type", type=str, help="Type of customer", required=True)

    args = parser.parse_args()

    exec(f"from configs import {args.customer_type.lower()}_config")
    config = eval(f"{args.customer_type.lower()}_config")

    # dictionary of clustering algorithms
    clustering_algorithms = {
        "k_means": KMeans,
        "gaussian_mixture": GaussianMixture,
        "db_scan": DBSCAN,
    }

    # get data from postgresql
    df_customer = get_data_from_db(query=f"SELECT * FROM {config.TABLE_NAME}", out_type="df")
    # pre-process the data
    data = pre_processing(df_customer, args)

    # get current path of this file
    current_path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(current_path, "models")):
        os.mkdir(os.path.join(current_path, "models"))

    # train the model
    for algorithm in tqdm(config.MODEL_CONFIG.keys(), desc="Training model: "):
        print(f"Training model for {algorithm}...")
        model = clustering_algorithms[algorithm](**config.MODEL_CONFIG[algorithm])
        model.fit(data)
        model_path = os.path.join(current_path, "models", f"{args.customer_type}_{algorithm}.pkl")
        save_pkl(data=model, file_path=model_path)
        print(f"Model for {algorithm} has been saved")

    print(f"Model for {args.customer_type} customer has been saved")
