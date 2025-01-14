import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Ensure the correct path to the CSV file is provided
df = pd.read_csv("data/nobel.csv")
print(df.info())
print("\n")

# Count the occurrences of each sex and find the maximum occurence
sex_counts = df["sex"].value_counts()
top_gender = sex_counts.index[0]

print(f"Most commonly awarded gender: {top_gender}")

#Visualize
g = sns.countplot(data=df, x="sex")
g.set(title="Distribution of Nobel Prize Winners by Gender",
      xlabel="Gender",
      ylabel="Count")

# Count the occurences of each country and find the maximum occurence
top_country = df["birth_country"].value_counts().index[0]
print(f"Most commonly awarded country: {top_country}")
print("\n")

#Which decade had the highest ratio of US-born Nobel Prize winners to total winners in all categories?

# Create decade column temporarily
df["decade"] = (df["year"] // 10) * 10
usa_winners = df[df["birth_country"] == "United States of America"].groupby("decade").size()
total_winners = df.groupby("decade").size()
usa_ratio = (usa_winners / total_winners)

# Find the decade with highest ratio
max_decade_usa = usa_ratio.idxmax()
print(f"Decade with highest ratio of US-born winners: {max_decade_usa}s")
print(f"Ratio: {usa_ratio[max_decade_usa]:.2%}\n")

# Reset index to make decade a column
usa_winners_df = usa_winners.reset_index(name="count")
usa_winners_df.rename(columns={"index": "decade"}, inplace=True)

# Create the plot
g = sns.catplot(
    data=usa_winners_df,
    x="decade",
    y="count",
    kind="bar",
)
g.set(xlabel="Decade", ylabel="Number of US born Nobel Prize Winners")
plt.xticks(rotation=90)

# Calculate proportion of female winners by decade and category
female_winners = df[df["sex"] == "Female"].groupby(["decade", "category"]).size()
total_by_decade_cat = df.groupby(["decade", "category"]).size()
female_ratio = (female_winners / total_by_decade_cat).fillna(0)

# Find the decade-category with highest female ratio
max_ratio_idx = female_ratio.idxmax()
max_ratio = female_ratio.max()

max_female_dict = {max_ratio_idx[0]: max_ratio_idx[1]}

print(f"\nDecade-Category with highest proportion of female laureates:")
print(f"{max_ratio_idx[0]}s - {max_ratio_idx[1]}")
print(f"Female proportion: {max_ratio:.2%}\n")

# Create a pivot table for visualization
female_ratio_pivot = female_ratio.reset_index()
female_ratio_pivot.columns = ["decade", "category", "proportion"]
female_ratio_pivot = female_ratio_pivot.pivot(index="decade", columns="category", values="proportion")

# Visualize the proportions
plt.figure(figsize=(12, 6))
sns.heatmap(female_ratio_pivot, 
            cmap="YlOrRd",
            annot=True, 
            fmt=".1%",
            cbar_kws={'label': 'Proportion of Female Laureates'})
plt.title("Proportion of Female Nobel Laureates by Decade and Category")
plt.ylabel("Decade")
plt.xlabel("Category")
plt.xticks(rotation=45)

# Drop the decade column
df.drop("decade", axis=1, inplace=True)

#Who was the first woman to receive a Nobel Prize, and in what category?
first_woman = df[df["sex"] == "Female"].sort_values("year").iloc[0]
first_woman_name = first_woman["full_name"]
first_woman_category = first_woman["category"]
print(f"{first_woman_name} - {first_woman_category}\n")

#Which individuals or organizations have won more than one Nobel Prize throughout the years?
winners_names = df["full_name"].value_counts()
repeat_list = winners_names[winners_names > 1].index.tolist()
print(repeat_list)
