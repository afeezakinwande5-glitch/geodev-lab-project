import pandas as pd

df = pd.read_csv("world_population.csv")

# Filter wards with population above 10,000
high_population = df[df["2022 Population"] > 3000000]

print("High population wards:")
print(high_population)

# Sort population from highest to lowest
sorted_data = df.sort_values(
    by="2022 Population",
    ascending=False
)

print("Sorted wards:")
print(sorted_data)