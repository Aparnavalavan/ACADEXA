import pandas as pd
from pathlib import Path

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("dataset/student_lifestyle_dataset.csv")

print("ACADEXA DATASET LOADED!")
print("Original Shape:", df.shape)

# ==========================================
# 2. CHECK MISSING VALUES
# ==========================================

print("\nMISSING VALUES BEFORE CLEANING:")
print(df.isnull().sum())

# ==========================================
# 3. REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()

print("\nDuplicates removed.")
print("Current Shape:", df.shape)

# ==========================================
# 4. CONVERT NUMERICAL COLUMNS
# ==========================================

numeric_columns = [
    "Study_Hours_Per_Day",
    "Extracurricular_Hours_Per_Day",
    "Sleep_Hours_Per_Day",
    "Social_Hours_Per_Day",
    "Physical_Activity_Hours_Per_Day",
    "Stress_Score",
    "Attendance_Percentage",
    "GPA"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================
# 5. HANDLE MISSING TARGET VALUES
# ==========================================

df = df.dropna(
    subset=["GPA", "Academic_Performance_Level"]
)

# ==========================================
# 6. HANDLE MISSING INPUT VALUES
# ==========================================

feature_columns = [
    "Study_Hours_Per_Day",
    "Extracurricular_Hours_Per_Day",
    "Sleep_Hours_Per_Day",
    "Social_Hours_Per_Day",
    "Physical_Activity_Hours_Per_Day",
    "Stress_Score",
    "Attendance_Percentage"
]

for col in feature_columns:
    df[col] = df[col].fillna(df[col].median())

# ==========================================
# 7. CLEAN PERFORMANCE LABELS
# ==========================================

df["Academic_Performance_Level"] = (
    df["Academic_Performance_Level"]
    .astype(str)
    .str.strip()
    .str.title()
)

valid_levels = ["Low", "Medium", "High"]

df = df[
    df["Academic_Performance_Level"].isin(valid_levels)
].copy()

# ==========================================
# 8. CHECK FINAL MISSING VALUES
# ==========================================

print("\nMISSING VALUES AFTER CLEANING:")
print(df.isnull().sum())

# ==========================================
# 9. SAVE CLEANED DATASET
# ==========================================

Path("dataset").mkdir(exist_ok=True)

df.to_csv(
    "dataset/cleaned_student_lifestyle_dataset.csv",
    index=False
)

# ==========================================
# 10. FINAL SUMMARY
# ==========================================

print("\n================================")
print("ACADEXA DATA CLEANING COMPLETED")
print("================================")

print("Final Dataset Shape:", df.shape)

print("\nAcademic Performance Distribution:")
print(df["Academic_Performance_Level"].value_counts())

print("\nCleaned dataset saved successfully!")