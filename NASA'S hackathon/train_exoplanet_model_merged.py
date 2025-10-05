import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 1) Load merged dataset
df = pd.read_csv("exoplanets_merged.csv")

# 2) Map mission (text) -> numeric code
mission_map = {"Kepler": 0, "K2": 1, "TESS": 2}
df["mission_code"] = df["mission"].map(mission_map).fillna(-1)

# 3) Feature list (use mission_code instead of mission)
features = [
    "orbital_period","transit_duration","transit_depth","planet_radius",
    "stellar_logg","stellar_radius","insolation","eq_temp","mag","model_snr",
    "ra","dec","mission_code","stellar_teff"
]

X = df[features].copy()
y = df["koi_disposition"].astype(str)

# 4) Fill missing values with medians (models can't handle NaN)
medians = X.median(numeric_only=True)
X = X.fillna(medians)

# 5) Split & train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300, random_state=42, class_weight="balanced", n_jobs=-1
)
model.fit(X_train, y_train)

# 6) Evaluate
y_pred = model.predict(X_test)
print("\n=== Model Report (merged) ===")
print(classification_report(y_test, y_pred))

# 7) Save bundle
bundle = {
    "model": model,
    "features": features,
    "medians": medians,
    "classes": model.classes_,
    "mission_map": mission_map
}
joblib.dump(bundle, "exoplanet_model_merged.joblib")
print("\nSaved: exoplanet_model_merged.joblib")
