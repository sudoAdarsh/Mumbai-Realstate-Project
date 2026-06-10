# Cleaning final master dataset

import pandas as pd

df = pd.read_csv("mumbai_real_estate_dataset.csv")

print("--- SHAPE ---")
print(df.shape)
print("--- INFO ---")
print(df.info())
print("--- IS NULL ---")
print(df.isnull().sum())
print("--- DESCRIBE ---")
print(df.describe())
