# clean_tess_data.py
import pandas as pd
import numpy as np

INPUT_CSV  = "tess.csv"   # <-- change to your TESS raw filename
OUTPUT_CSV = "cleaned_tess.csv"

# Read robustly: ignore '#' comment lines, auto-detect delimiter (tab/comma), skip bad lines
df = pd.read_csv(
    INPUT_CSV,
    comment="#",
    engine="python",
    sep=None,
    on_bad_lines="skip"
)

# TESS uses 'tfopwg_disp' with codes: PC, FP, CP, KP
if "tfopwg_disp" not in df.columns:
    raise ValueError("Column 'tfopwg_disp' not found. Check your TESS file or header line.")

# Map TESS dispositions to Kepler-like labels
map_disp = {
    "PC": "CANDIDATE",
    "FP": "FALSE POSITIVE",
    "CP": "CONFIRMED",
    "KP": "CONFIRMED"
}

# Create koi_disposition column
df["koi_disposition"] = df["tfopwg_disp"].map(map_disp)

# Keep only rows with a valid mapped label
df = df[df["koi_disposition"].notna()].copy()

# Keep only numeric columns for features
num_df = df.select_dtypes(include=[np.number]).copy()

# Drop columns that are too empty (>=70% non-null kept)
keep_cols = num_df.columns[num_df.notna().mean() >= 0.70]
num_df = num_df[keep_cols]

# Fill remaining missing values with medians
medians = num_df.median(numeric_only=True)
num_df = num_df.fillna(medians)

# Add back the target column as last column
cleaned = pd.concat([num_df, df[["koi_disposition"]]], axis=1)

# Save
cleaned.to_csv(OUTPUT_CSV, index=False)

# Summary
print("TESS Input shape:", df.shape)
print("Numeric features kept:", len(num_df.columns))
print("TESS Output shape:", cleaned.shape)
print("Saved:", OUTPUT_CSV)
print("\nLabel counts:")
print(cleaned["koi_disposition"].value_counts())
