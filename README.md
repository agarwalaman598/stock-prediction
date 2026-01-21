# Live Stock Price Prediction
### Linear Regression & LSTM with Real-Time Data

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=flat-square)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0%2B-orange?style=flat-square)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

A robust machine learning application designed to forecast next-day stock closing prices using real-time market data. Built on a Flask backend, this project implements and compares **Linear Regression** and **Long Short-Term Memory (LSTM)** neural networks to provide actionable insights across global financial markets.

---

## 🚀 Feature Highlights

- **Real-Time Data Ingestion**: Seamless integration with Yahoo Finance (`yfinance`) for up-to-the-minute market data.
- **Dual-Model Inference**: Simultaneous execution of statistical (Linear Regression) and deep learning (LSTM) models for comparative analysis.
- **Global Market Support**: Full compatibility with international tickers (e.g., NSE, BSE, LSE, NASDAQ).
- **Interactive Web Interface**: A minimal, responsive frontend with line-chart visualization of historical prices and predicted next-day close.
- **Automated Preprocessing**: On-the-fly data cleaning, normalization, and sequence generation.

---



## 📂 Folder Structure

```text
stock-prediction/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── model_lr.py         # Linear Regression training script
│   ├── model_lstm.py       # LSTM training script
│   ├── templates/
│   │   └── index.html      # Frontend UI
│   └── static/
│       ├── script.js       # Client-side logic
│       └── style.css       # Styling
├── data/
│   └── stock_data.csv      # Local data cache (optional)
├── requirements.txt        # Project dependencies
└── venv/                   # Virtual environment
```

---

## 🏗️ System Architecture
```text
User
 ↓
Web UI (HTML / CSS / JavaScript)
 ↓
Flask Backend (REST API)
 ↓
Yahoo Finance (Live Market Data)
 ↓
ML Models (Linear Regression + LSTM)
 ↓
Prediction + Visualization (Chart.js)

```
---



## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/stock-prediction.git
cd stock-prediction
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧠 Model Training

Before running the application, train the models to generate the necessary `.keras` and `.pkl` model files.

```bash
# Train Linear Regression Model
python backend/model_lr.py

# Train LSTM Model
python backend/model_lstm.py
```

> **Note:** Training may take a few minutes depending on your hardware.

---

## ▶️ Running the Application

Start the Flask server:

```bash
python backend/app.py
```

Access the application at `http://127.0.0.1:5000` in your browser.

---

## 🖼️ Screenshots

<div align="center">

### Dashboard Interface

<img src="assets/screenshot-1.png" alt="Dashboard Interface" width="700"/>

### Enter Stock Symbol

<img src="assets/screenshot-2.png" alt="Model Loading" width="700"/>

### Prediction

<img src="assets/screenshot-3.png" alt="Analysis Results" width="700"/>

</div>

---

## 🌍 How to Enter Stock Symbols

This application supports global markets via Yahoo Finance tickers. Use the correct suffix for your target market:

| Country | Market | Suffix | Example |
| :--- | :--- | :--- | :--- |
| **USA** | NASDAQ/NYSE | *None* | `AAPL`, `TSLA` |
| **India** | NSE | `.NS` | `RELIANCE.NS` |
| **India** | BSE | `.BO` | `TCS.BO` |
| **UK** | LSE | `.L` | `BARC.L` |
| **Canada** | TSX | `.TO` | `SHOP.TO` |

---

## 📊 What the Prediction Means

- **Prediction Target**: The model predicts the **Closing Price** for the **Next Trading Day**.
- **Live Price**: The current real-time price displayed for reference.
- **Interpretation**: If `Predicted Price > Live Price`, the trend is bullish. If `Predicted Price < Live Price`, the trend is bearish.

---

## 🤖 Models Used

### 1. Linear Regression
- **Type**: Statistical.
- **Use Case**: Establishes a baseline trend line.
- **Pros**: Fast, interpretable, good for short-term linear trends.

### 2. Long Short-Term Memory (LSTM)
- **Type**: Recurrent Neural Network (RNN).
- **Use Case**: Captures complex, non-linear temporal dependencies in time-series data.
- **Pros**: Handles sequential data effectively, learns long-term patterns.

---

## 📈 Model Evaluation

Both models are evaluated using standard regression error metrics on a held-out test set:

- **MAE (Mean Absolute Error)** — Average absolute prediction error
- **RMSE (Root Mean Square Error)** — Penalizes larger errors more strongly

Run evaluation:
```bash
python backend/evaluate_models.py
```
### Sample Output

```text
Linear Regression:
MAE  : 2.4
RMSE : 3.47

LSTM:
MAE  : 6.04
RMSE : 7.88
```

> Note: Values vary depending on the dataset, training window, and market conditions.


---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. The predictions generated by these models should **not** be used as the sole basis for financial decisions. Stock markets are volatile and influenced by unpredictable factors.


---

## 👨‍💻 Author

**Aman Agarwal**

---


