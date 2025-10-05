# clean_exoplanet_data.py
import pandas as pd
import numpy as np

# --- paths ---
INPUT_CSV  = "kepler_koi_cumulative.csv"      # change if your filename is different
OUTPUT_CSV = "cleaned_exoplanet_data.csv"

# 1) read raw csv (tolerant to comments/bad lines)
df = pd.read_csv(
    INPUT_CSV,
    comment="#",
    engine="python",
    on_bad_lines="skip"
)

# keep only rows that actually have the target label
df = df[df["koi_disposition"].notna()]

# 2) keep only numeric feature columns (models use numbers)
num_df = df.select_dtypes(include=[np.number]).copy()

# drop "too empty" numeric columns (keep columns with ≥ 70% non-null)
keep_cols = num_df.columns[num_df.notna().mean() >= 0.70]
num_df = num_df[keep_cols]

# fill remaining missing numeric values with column medians
medians = num_df.median(numeric_only=True)
num_df = num_df.fillna(medians)

# 3) add back the target column (as the last column)
cleaned = pd.concat([num_df, df[["koi_disposition"]]], axis=1)

# 4) save cleaned csv
cleaned.to_csv(OUTPUT_CSV, index=False)

# friendly summary
print("Input shape:", df.shape)
print("Numeric features kept:", len(num_df.columns))
print("Output shape:", cleaned.shape)
print("Saved:", OUTPUT_CSV)
print("\nLabel counts:")
print(df["koi_disposition"].value_counts())
