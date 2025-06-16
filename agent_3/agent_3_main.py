import os
import json
import gspread
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()  # ✅ Carga automática de .env


def connect_to_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    if not creds_json:
        raise Exception("Google Sheets credentials not found in environment variables.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def load_signals(sheet_name: str, tab_name: str) -> pd.DataFrame:
    client = connect_to_google_sheets()
    worksheet = client.open(sheet_name).worksheet(tab_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def analyze_signals(df: pd.DataFrame, symbol: str) -> str:
    latest = df.tail(1).iloc[0]
    rsi = latest.get("RSI", None)
    ema10 = latest.get("EMA_10", None)
    ema20 = latest.get("EMA_20", None)
    compra = int(latest.get("compra1", 0))
    venta = int(latest.get("venta1", 0))

    if rsi is None or ema10 is None:
        return f"Insufficient data to analyze {symbol}."

    if compra:
        return f"BUY {symbol} (RSI={rsi}, EMA10>EMA20)"
    elif venta:
        return f"SELL {symbol} (RSI={rsi}, EMA10<EMA20)"
    else:
        return f"KEEP {symbol} (RSI={rsi})"

def write_recommendations(sheet_name: str, recommendations: list):
    client = connect_to_google_sheets()
    spreadsheet = client.open(sheet_name)

    try:
        worksheet = spreadsheet.worksheet("Recomendaciones")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="Recomendaciones", rows="100", cols="2")

    df = pd.DataFrame(recommendations, columns=["Símbolo", "Recomendación"])
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print("✅ Recommendations written in the 'Recommendations' tab.")

def main():
    sheet_name = "Diary"
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]

    print("\n===== Agent 3 - Financial Recommender =====\n")
    all_recommendations = []

    for symbol in symbols:
        try:
            df = load_signals(sheet_name, symbol)
            if df.empty or 'Close' not in df.columns:
                print(f"{symbol}:Insufficient data.")
                continue

            recommendation = analyze_signals(df, symbol)
            print(f"{symbol}: {recommendation}")
            all_recommendations.append((symbol, recommendation))

        except Exception as e:
            print(f"{symbol}: Error processing - {e}")

    write_recommendations(sheet_name, all_recommendations)

if __name__ == "__main__":
    main()

