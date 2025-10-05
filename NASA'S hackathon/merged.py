import pandas as pd

# ==== INPUT FILES (your cleaned files) ====
KEPLER_CSV = "kepler_cleaned.csv"
K2_CSV     = "k2_cleaned.csv"
TESS_CSV   = "tess_cleaned.csv"

# ==== OUTPUT ====
OUT_CSV = "exoplanets_merged.csv"

# ==== Unified column list (target + features we’ll keep) ====
unified_cols = [
    # labels
    "koi_disposition",
    # core planet transit/size
    "orbital_period",      # days (koi_period / pl_orbper)
    "transit_duration",    # hours (koi_duration / pl_trandurh)
    "transit_depth",       # ppm   (koi_depth / pl_trandep)
    "planet_radius",       # R_earth (koi_prad / pl_rade)
    # star properties
    "stellar_teff",        # K (koi_steff / st_teff)
    "stellar_logg",        # cgs (koi_slogg / st_logg)
    "stellar_radius",      # R_sun (koi_srad / st_rad)
    # helpful extras if present
    "insolation",          # Earth flux (koi_insol / pl_insol)
    "eq_temp",             # K (koi_teq / pl_eqt)
    "mag",                 # magnitude (koi_kepmag / st_tmag / sy_vmag)
    "model_snr",           # Kepler SNR (koi_model_snr) — only in Kepler
    # positioning (optional but shared)
    "ra",                  # degrees
    "dec"                  # degrees
]

# ==== Per-mission rename maps → unified names ====
kepler_map = {
    "koi_period":     "orbital_period",
    "koi_duration":   "transit_duration",
    "koi_depth":      "transit_depth",
    "koi_prad":       "planet_radius",
    "koi_teff":       "stellar_teff",
    "koi_slogg":      "stellar_logg",
    "koi_srad":       "stellar_radius",
    "koi_insol":      "insolation",
    "koi_teq":        "eq_temp",
    "koi_kepmag":     "mag",
    "koi_model_snr":  "model_snr",
    "ra":             "ra",
    "dec":            "dec"
}

k2_map = {
    "pl_orbper":  "orbital_period",
    # K2 doesn’t give duration/depth directly in your list → will be missing
    "pl_rade":    "planet_radius",
    "st_teff":    "stellar_teff",
    "st_rad":     "stellar_radius",
    "sy_vmag":    "mag",        # you also have sy_kmag/sy_gaiamag; we’ll standardize on Vmag
    "ra":         "ra",
    "dec":        "dec"
    # label already named koi_disposition by your cleaner
}

tess_map = {
    "pl_orbper":    "orbital_period",
    "pl_trandurh":  "transit_duration",
    "pl_trandep":   "transit_depth",
    "pl_rade":      "planet_radius",
    "pl_insol":     "insolation",
    "pl_eqt":       "eq_temp",
    "st_tmag":      "mag",
    "st_teff":      "stellar_teff",
    "st_logg":      "stellar_logg",
    "st_rad":       "stellar_radius",
    "ra":           "ra",
    "dec":          "dec"
}

# ==== Load ====
kepler = pd.read_csv(KEPLER_CSV)
k2     = pd.read_csv(K2_CSV)
tess   = pd.read_csv(TESS_CSV)

# ==== Rename to unified names ====
kepler_std = kepler.rename(columns=kepler_map)
k2_std     = k2.rename(columns=k2_map)
tess_std   = tess.rename(columns=tess_map)

# ==== Select only the unified columns that actually exist in each file ====
k_keep   = [c for c in unified_cols if c in kepler_std.columns]
k2_keep  = [c for c in unified_cols if c in k2_std.columns]
t_keep   = [c for c in unified_cols if c in tess_std.columns]

kepler_std = kepler_std[k_keep].copy()
k2_std     = k2_std[k2_keep].copy()
tess_std   = tess_std[t_keep].copy()

# ==== Add mission tag (optional, helps analysis) ====
kepler_std["mission"] = "Kepler"
k2_std["mission"]     = "K2"
tess_std["mission"]   = "TESS"

# ==== Merge rows ====
merged = pd.concat([kepler_std, k2_std, tess_std], ignore_index=True)

# ==== Drop rows without label (safety) ====
merged = merged[merged["koi_disposition"].notna()].reset_index(drop=True)

# ==== Save ====
merged.to_csv(OUT_CSV, index=False)

# ==== Quick summary ====
print("Merged shape:", merged.shape)
print("\nColumns:", list(merged.columns))
print("\nLabel counts:")
print(merged["koi_disposition"].value_counts())
print(f"\nSaved → {OUT_CSV}")
