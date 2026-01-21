import yfinance as yf
from flask import Flask, jsonify, render_template
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load models
lr_model = joblib.load("saved_models/linear_model.pkl")
lstm_model = load_model("saved_models/lstm_model.keras", compile=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict/<symbol>")
@app.route("/predict/<symbol>")
def predict_symbol(symbol):
    try:
        # Download data
        data = yf.download(symbol, period="3mo", progress=False)

        if data is None or data.empty:
            return jsonify({"error": "No data returned for this symbol"}), 400

        # Fix MultiIndex columns from yfinance
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if "Close" not in data.columns:
            return jsonify({"error": "Close price not found"}), 400

        # Convert Close to numeric Series safely
        close_series = pd.to_numeric(data["Close"].squeeze(), errors="coerce")
        close_series = close_series.dropna()

        if len(close_series) < 60:
            return jsonify({"error": "Not enough valid price data"}), 400

        # Convert to NumPy
        prices = close_series.to_numpy(dtype=np.float64).reshape(-1, 1)

        # Local min-max scaling
        min_price = float(np.min(prices))
        max_price = float(np.max(prices))

        if max_price <= min_price:
            return jsonify({"error": "Invalid price range"}), 400

        scaled_prices = (prices - min_price) / (max_price - min_price)
        last_60 = scaled_prices[-60:]

        # Linear Regression
        lr_input = last_60.reshape(1, -1)
        lr_scaled = float(lr_model.predict(lr_input).ravel()[0])

        # LSTM
        lstm_input = last_60.reshape(1, 60, 1)
        lstm_scaled = float(lstm_model.predict(lstm_input).ravel()[0])

        # Convert back to price
        lr_price = (lr_scaled * (max_price - min_price)) + min_price
        lstm_price = (lstm_scaled * (max_price - min_price)) + min_price

        return jsonify({
            "symbol": symbol.upper(),
            "linear_prediction": round(lr_price, 2),
            "lstm_prediction": round(lstm_price, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
