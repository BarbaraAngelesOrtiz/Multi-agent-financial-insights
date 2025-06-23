import os
import json
import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_indicators(df):
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df["RSI"] = calculate_rsi(df["Close"])
    df["EMA_10"] = df["Close"].ewm(span=10).mean()
    df["EMA_20"] = df["Close"].ewm(span=20).mean()
    df["EMA_40"] = df["Close"].ewm(span=40).mean()

    df["compra1"] = ((df["EMA_10"] > df["EMA_20"]) & (df["RSI"] < 60)).astype(int)
    df["compra2"] = ((df["EMA_10"] > df["EMA_20"]) & (df["EMA_20"] > df["EMA_40"])).astype(int)
    df["venta1"] = ((df["RSI"] > 70) & (df["Close"] < df["EMA_10"])).astype(int)
    df["venta2"] = ((df["RSI"] > 70) & (df["Close"] < df["EMA_20"])).astype(int)

    return df.round(2)

def main():
    print("🚀 Starting Agent 2 - Local Mode")

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)  # <-- línea agregada

    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]

    for symbol in symbols:
        input_path = os.path.join(data_dir, f"{symbol}_raw.json")
        output_path = os.path.join(data_dir, f"{symbol}_processed.json")

        if not os.path.exists(input_path):
            print(f"⚠️ {symbol}_raw.json not found. Skipping.")
            continue

        try:
            df = pd.read_json(input_path)
            df = calculate_indicators(df)
            df.to_json(output_path, orient="records")
            print(f"✅ Processed and saved {output_path}")
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")


if __name__ == "__main__":
    main()
