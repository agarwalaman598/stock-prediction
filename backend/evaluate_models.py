import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler

# Load models
lr_model = joblib.load("saved_models/linear_model.pkl")
lstm_model = load_model("saved_models/lstm_model.keras", compile=False)

# Load dataset
data = pd.read_csv("../data/stock_data.csv")

# Clean Close column
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

# Train/Test split
split = int(0.8 * len(X))
X_test = X[split:]
y_test = y[split:]

# ----- Linear Regression -----
X_test_lr = X_test.reshape(X_test.shape[0], -1)
lr_preds_scaled = lr_model.predict(X_test_lr).ravel()

# ----- LSTM -----
lstm_preds_scaled = lstm_model.predict(X_test).ravel()

# Inverse scaling
y_test_real = scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()
lr_preds_real = scaler.inverse_transform(lr_preds_scaled.reshape(-1, 1)).ravel()
lstm_preds_real = scaler.inverse_transform(lstm_preds_scaled.reshape(-1, 1)).ravel()

# Metrics
# Metrics
lr_mae = mean_absolute_error(y_test_real, lr_preds_real)
lr_rmse = np.sqrt(mean_squared_error(y_test_real, lr_preds_real))

lstm_mae = mean_absolute_error(y_test_real, lstm_preds_real)
lstm_rmse = np.sqrt(mean_squared_error(y_test_real, lstm_preds_real))


print("\nMODEL COMPARISON RESULTS\n")
print("Linear Regression:")
print("MAE  :", round(lr_mae, 2))
print("RMSE :", round(lr_rmse, 2))

print("\nLSTM:")
print("MAE  :", round(lstm_mae, 2))
print("RMSE :", round(lstm_rmse, 2))
