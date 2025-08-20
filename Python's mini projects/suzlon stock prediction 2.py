import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

df = yf.download("SUZLON.NS", start="2015-01-01", end="2025-01-01")

data = pd.DataFrame()
data["ds"] = df.index
data["y"] = df["Close"].values
data = data.dropna()

model = Prophet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True)
model.fit(data)

future = model.make_future_dataframe(periods=1825)
forecast = model.predict(future)

plt.figure(figsize=(12,6))
plt.plot(data["ds"], data["y"], color="red", label="Actual Price")  # Red = Actual
plt.plot(forecast["ds"], forecast["yhat"], color="blue", label="Predicted Price")  # Blue = Predicted
plt.xlabel("Date")
plt.ylabel("Suzlon Stock Price (INR)")
plt.title("Suzlon Stock Price Prediction (Actual vs Forecast)")
plt.legend()
plt.grid(True)
plt.show()

model.plot_components(forecast)
plt.show()