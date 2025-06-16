import os
import json
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet_data(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    if not creds_json:
        raise Exception("Google Sheets credentials JSON not found in environment variables.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1

    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df, sheet

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_sma(series, period=14):
    return series.rolling(window=period).mean()

def main():
    print("Starting Agent 2 - Data Processing...")

    sheet_name = 'Diario'  # Cambia acá al nombre exacto de tu hoja

    df, sheet = get_sheet_data(sheet_name)
    print(f"Data loaded: {len(df)} rows")

    # Suponiendo que hay columna 'close' con precios de cierre
    if 'close' not in df.columns:
        raise Exception("Column 'close' not found in sheet data")

    df['RSI_14'] = calculate_rsi(df['close'])
    df['SMA_14'] = calculate_sma(df['close'], 14)
    df['SMA_7'] = calculate_sma(df['close'], 7)

    print("Indicators calculated.")

    # Actualizamos Google Sheet (podés ajustar rango o columnas según tu formato)
    # Ejemplo simple: sobreescribir toda la hoja (incluyendo encabezados)
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.fillna('').values.tolist())

    print("Google Sheet updated successfully.")

if __name__ == "__main__":
    main()
