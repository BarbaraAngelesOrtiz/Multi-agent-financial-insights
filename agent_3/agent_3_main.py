import os
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'creds.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
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

    if rsi is None or ema10 is None or ema20 is None:
        return f"{symbol}: Datos incompletos"

    if rsi < 30 and ema10 > ema20:
        return f"{symbol}: Señal de COMPRA"
    elif rsi > 70 and ema10 < ema20:
        return f"{symbol}: Señal de VENTA"
    else:
        return f"{symbol}: Sin señal clara"

def main():
    sheet_name = "Financial Signals"
    tab_name = "Diary"
    symbol = "AAPL"  # O el que corresponda

    os.makedirs("data", exist_ok=True)  # <-- línea agregada

    try:
        df = load_signals(sheet_name, tab_name)
        result = analyze_signals(df, symbol)
        print(result)

        # Guardar resultado para subir como artifact
        with open("data/analysis_result.txt", "w", encoding="utf-8") as f:
            f.write(result)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
