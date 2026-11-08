import pandas as pd

#Read CSV
df = pd.read_csv("NGA_adm2.csv")

# Display the data
print(df)

# First five records
print(df.head())

#Dataset information
print(df.info())

# Statistical summary
print(df.describe())

# Numbers of rows and columns
print(df.shape)

# Column names
print(df.columns)
