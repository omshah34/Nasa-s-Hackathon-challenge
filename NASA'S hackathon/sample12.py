# clean_k2_data.py
import pandas as pd
import numpy as np

# --- paths ---
INPUT_CSV  = "k2.csv"          # change to your actual K2 raw filename
OUTPUT_CSV = "k2_cleaned.csv"

# 1) read raw csv (tolerant to comments/bad lines)
df = pd.read_csv(
    INPUT_CSV,
    comment="#",
    engine="python",
    on_bad_lines="skip"
)

# keep only rows that actually have the target label
if "koi_disposition" in df.columns:
    df = df[df["koi_disposition"].notna()]
elif "disposition" in df.columns:   # some K2/TESS use 'disposition'
    df = df[df["disposition"].notna()]
    df = df.rename(columns={"disposition": "koi_disposition"})

# 2) keep only numeric feature columns
num_df = df.select_dtypes(include=[np.number]).copy()

# drop "too empty" numeric columns
keep_cols = num_df.columns[num_df.notna().mean() >= 0.70]
num_df = num_df[keep_cols]

# fill missing values with medians
medians = num_df.median(numeric_only=True)
num_df = num_df.fillna(medians)

# 3) add back target column
cleaned = pd.concat([num_df, df[["koi_disposition"]]], axis=1)

# 4) save
cleaned.to_csv(OUTPUT_CSV, index=False)

print("Input shape:", df.shape)
print("Numeric features kept:", len(num_df.columns))
print("Output shape:", cleaned.shape)
print("Saved:", OUTPUT_CSV)
print("\nLabel counts:")
print(df["koi_disposition"].value_counts())
