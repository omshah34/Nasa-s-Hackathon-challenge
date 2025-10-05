import pandas as pd
import joblib

# Load trained bundle
bundle = joblib.load("exoplanet_model_merged.joblib")
model     = bundle["model"]
features  = bundle["features"]
medians   = bundle["medians"]
classes   = list(bundle["classes"])
mission_map = bundle["mission_map"]

print("\n=== Exoplanet Prediction (Kepler / K2 / TESS) ===")
telescope = input("Which telescope? (Kepler/K2/TESS): ").strip()

# map telescope -> mission_code
mission_code = mission_map.get(telescope, -1)

# Decide whether to ask for stellar_teff
ask_teff = telescope.lower() in ["k2", "tess"]

# Build interactive input row
row = {}

def ask_num(col):
    val = input(f"{col} (Enter to use median): ").strip()
    if val == "":
        return float(medians.get(col, 0))
    try:
        return float(val)
    except:
        return float(medians.get(col, 0))

# Always-asked features
for col in [
    "orbital_period","transit_duration","transit_depth","planet_radius",
    "stellar_logg","stellar_radius","insolation","eq_temp","mag","model_snr",
    "ra","dec"
]:
    if col in features:
        row[col] = ask_num(col)

# Mission code (numeric)
row["mission_code"] = mission_code if "mission_code" in features else 0.0

# stellar_teff only for K2/TESS
if ask_teff and "stellar_teff" in features:
    row["stellar_teff"] = ask_num("stellar_teff")
else:
    # fill with median if not asked or not present
    if "stellar_teff" in features:
        row["stellar_teff"] = float(medians.get("stellar_teff", 0))

# Fill any missing feature with median
for col in features:
    if col not in row:
        row[col] = float(medians.get(col, 0))

# Predict
X = pd.DataFrame([row], columns=features)
proba = model.predict_proba(X)[0]
pred  = model.predict(X)[0]

# Pretty print
out = pd.DataFrame({"Class": classes, "Probability_%": (proba*100).round(2)}).sort_values(
    "Probability_%", ascending=False
)
print("\n=== Prediction Results ===")
print(out.to_string(index=False))
print("\nPredicted Class:", pred)
