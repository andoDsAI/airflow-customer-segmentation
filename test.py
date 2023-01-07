import pandas as pd

df = pd.read_csv("src/data/e_commerce_customers.csv", encoding="unicode_escape")
print(df.head())
