import yfinance as yf
import pandas as pd

def download_data(symbol="AAPL", start="2015-01-01"):
    data = yf.download(symbol, start=start)
    data.to_csv("../data/stock_data.csv")
    print("Data saved to data/stock_data.csv")

if __name__ == "__main__":
    download_data()