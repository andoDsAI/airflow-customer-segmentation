import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_type", type=str, help="Type of customer", required=True)

    args = parser.parse_args()
    print("Crawler is running...")
