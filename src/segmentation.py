import argparse
import copy
import os

from tqdm import tqdm

tqdm.pandas()

from utils.helpers import get_data_from_db, insert_data_to_db, load_pkl, truncate_table

current_path = os.path.dirname(os.path.abspath(__file__))


def predict(df, model, config, algorithm):
    training_columns = config.TRAINING_COLUMNS
    categorical_columns = config.CATEGORICAL_COLUMNS

    label_encoders = {}
    for col in categorical_columns:
        encoder_path = os.path.join(
            current_path, f"models/{args.customer_type}_{col}_label_encoder.pkl"
        )
        label_encoders[col] = load_pkl(file_path=encoder_path)

    scaler_path = os.path.join(current_path, f"models/{args.customer_type}_scaler.pkl")
    standard_scaler = load_pkl(file_path=scaler_path)

    def get_predict(row):
        x = copy.deepcopy(row[training_columns])
        for col in categorical_columns:
            x[col] = label_encoders[col].transform([x[col]])[0]
        x = standard_scaler.transform([x])
        return model.predict(x)[0]

    df[f"{algorithm}_cluster"] = df.progress_apply(get_predict, axis=1)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_type", type=str, help="Type of customer", required=True)

    args = parser.parse_args()
    exec(f"from configs import {args.customer_type.lower()}_config")
    config = eval(f"{args.customer_type.lower()}_config")

    data = get_data_from_db(
        query=f"SELECT * FROM {config.TABLE_NAME}",
        out_type="df",
    )

    algorithms = config.MODEL_CONFIG.keys()
    for algorithm in algorithms:
        model_path = os.path.join(current_path, f"models/{args.customer_type}_{algorithm}.pkl")
        model = load_pkl(file_path=model_path)
        data = predict(data, model, config, algorithm)

    # truncate table
    truncate_table(table_name=config.TABLE_NAME)

    # insert data to db
    insert_data_to_db(table_name=config.TABLE_NAME, data=data)
