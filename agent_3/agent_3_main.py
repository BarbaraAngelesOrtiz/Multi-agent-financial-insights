# agent_3/main.py - Agente ADK que genera recomendaciones desde Google Sheets

import os
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# === FUNCIONES BASE ===
def connect_to_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
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
        return f"Datos insuficientes para analizar {symbol}."

    if compra:
        return f"Recomendación: COMPRAR {symbol}. RSI={rsi}, EMA10 > EMA20."
    elif venta:
        return f"Recomendación: VENDER {symbol}. RSI={rsi}, EMA10 < EMA20."
    else:
        return f"{symbol}: No hay señal clara hoy. RSI={rsi}."

# === MAIN ===
def main():
    sheet_name = "Diary"
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]

    print("\n===== Agente 3 - Generador de Recomendaciones =====\n")
    for symbol in symbols:
        try:
            df = load_signals(sheet_name, symbol)
            if df.empty:
                print(f"{symbol}: Sin datos.")
                continue
            recommendation = analyze_signals(df, symbol)
            print(recommendation)
        except Exception as e:
            print(f"Error con {symbol}: {e}")

if __name__ == "__main__":
    main()
