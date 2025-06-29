import os
import json
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

    df["buy1"] = ((df["EMA_10"] > df["EMA_20"]) & (df["RSI"] < 60)).astype(int)
    df["buy2"] = ((df["EMA_10"] > df["EMA_20"]) & (df["EMA_20"] > df["EMA_40"])).astype(int)
    df["sell1"] = ((df["RSI"] > 70) & (df["Close"] < df["EMA_10"])).astype(int)
    df["sell2"] = ((df["RSI"] > 70) & (df["Close"] < df["EMA_20"])).astype(int)

    return df.round(2)

def connect_to_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS_MULTI')
    if not creds_json:
        raise Exception("Google Sheets credentials not found in environment variables.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def main():
    print("🚀 Starting Agent 2 - Technical Analysis")

    sheet_name = "Stocks"
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]

    client = connect_to_sheets()
    spreadsheet = client.open(sheet_name)

    for symbol in symbols:
        try:
            worksheet = spreadsheet.worksheet(symbol)
            print(f"📥 Reading data for: {symbol}")

            data = worksheet.get_all_records()
            if not data:
                print(f"⚠️ Tab '{symbol}' is empty. Skipping.")
                continue

            df = pd.DataFrame(data)

            if 'Close' not in df.columns:
                print(f"⚠️Column 'Close' not found in {symbol}. Skipping.")
                continue

            df = calculate_indicators(df)

            # Update sheet (without doing .clear())
            worksheet.update([df.columns.values.tolist()] + df.fillna('').values.tolist())
            print(f"✅ Aggregate indicators in'{symbol}'")

        except Exception as e:
            print(f"⚠️ Error {symbol}: {e}")

if __name__ == "__main__":
    main()
