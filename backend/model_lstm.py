import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
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

# Model
model = Sequential()
model.add(Input(shape=(60, 1)))
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(optimizer="adam", loss="mse")

# Train
model.fit(X, y, epochs=5, batch_size=32)

# Save
model.save("saved_models/lstm_model.keras")
joblib.dump(scaler, "saved_models/scaler.pkl")

print("LSTM model and scaler saved.")
