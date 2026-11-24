import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_student_lifestyle_dataset.csv")

# Create results folder
Path("results").mkdir(exist_ok=True)

sns.set_theme(style="darkgrid")

# 1. Dataset Overview
print("\nDATASET INFORMATION")
print(df.info())

print("\nSTATISTICAL SUMMARY")
print(df.describe())

# 2. Academic Performance Distribution
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="Academic_Performance_Level")
plt.title("Academic Performance Distribution")
plt.savefig("results/performance_distribution.png")
plt.show()

# 3. Study Hours vs GPA
plt.figure(figsize=(7, 5))
sns.scatterplot(
    data=df,
    x="Study_Hours_Per_Day",
    y="GPA"
)
plt.title("Study Hours vs GPA")
plt.savefig("results/study_hours_vs_gpa.png")
plt.show()

# 4. Sleep Hours vs GPA
plt.figure(figsize=(7, 5))
sns.scatterplot(
    data=df,
    x="Sleep_Hours_Per_Day",
    y="GPA"
)
plt.title("Sleep Hours vs GPA")
plt.savefig("results/sleep_hours_vs_gpa.png")
plt.show()

# 5. Correlation Heatmap
plt.figure(figsize=(10, 7))
numeric_df = df.select_dtypes(include="number")
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Lifestyle Feature Correlation")
plt.tight_layout()
plt.savefig("results/correlation_heatmap.png")
plt.show()

print("\nEDA ANALYSIS COMPLETED SUCCESSFULLY!")