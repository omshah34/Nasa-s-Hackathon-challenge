import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

df = yf.download("SUZLON.NS", start="2018-01-01", end="2025-01-01")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.reset_index()

data = df[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
data["y"] = pd.to_numeric(data["y"], errors="coerce")  # force numeric

print("Sample data:")
print(data.head())

model = Prophet(daily_seasonality=True)
model.fit(data)

future = model.make_future_dataframe(periods=180)  # predict next 6 months
forecast = model.predict(future)

print("\nForecast Sample:")
print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())

fig1 = model.plot(forecast)
plt.title("Suzlon Energy Stock Price Prediction")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.show()

fig2 = model.plot_components(forecast)
plt.show()

comparison = data.merge(forecast[["ds", "yhat"]], on="ds", how="left")

plt.figure(figsize=(12,6))
plt.plot(comparison["ds"], comparison["y"], label="Actual Price", color="blue")
plt.plot(comparison["ds"], comparison["yhat"], label="Predicted Price", color="red")
plt.title("Suzlon Energy: Actual vs Predicted")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend()
plt.show()