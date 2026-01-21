import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load training data
data = pd.read_csv("../data/stock_data.csv")

data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
data = data.dropna()

prices = data["Close"].values.reshape(-1, 1)

# Scale
scaler = MinMaxScaler()
scaled_prices = scaler.fit_transform(prices)

# Create sequences
X, y = [], []
for i in range(60, len(scaled_prices)):
    X.append(scaled_prices[i-60:i])
    y.append(scaled_prices[i])

X = np.array(X)
y = np.array(y)

# Flatten for LR
X = X.reshape(X.shape[0], -1)

# Train
model = LinearRegression()
model.fit(X, y)

# Save
joblib.dump(model, "saved_models/linear_model.pkl")
joblib.dump(scaler, "saved_models/scaler.pkl")

print("Linear Regression model and scaler saved.")
