import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_type", type=str, help="Type of customer", required=True)

    args = parser.parse_args()
    exec(f"from configs import {args.customer_type.lower()}_config")
    config = eval(f"{args.customer_type.lower()}_config")

    print(config)
