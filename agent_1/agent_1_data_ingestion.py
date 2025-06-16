import os
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_alpha_vantage_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    # Verificamos que la respuesta sea correcta
    if "Time Series (Daily)" not in data:
        raise Exception(f"Alpha Vantage API error or limit reached: {data}")

    time_series = data["Time Series (Daily)"]

    # Extraemos la fecha más reciente
    latest_date = max(time_series.keys())

    # Obtenemos el valor "4. close" para la fecha más reciente
    latest_close = time_series[latest_date]["4. close"]

    # Devolvemos ese valor como float
    return float(latest_close)

def write_to_google_sheets(sheet_name, close_value):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    if not creds_json:
        raise Exception("Google credentials JSON not found in environment variables.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1

    # Aquí escribimos el valor en A1 (puedes cambiar la celda si quieres)
    sheet.update('A1', f"Latest Close: {close_value}")

def main():
    print("Starting Agent 1 - Data Ingestion...")

    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not alpha_key:
        raise Exception("Alpha Vantage API key not found in environment variables.")

    symbol = 'AAPL'  # Cambia el símbolo si quieres

    print(f"Fetching data for {symbol} from Alpha Vantage...")
    latest_close = get_alpha_vantage_data(symbol, alpha_key)
    print(f"Latest closing price for {symbol}: {latest_close}")

    sheet_name = 'Diario'  # Cambia por el nombre exacto de tu Google Sheet
    print("Writing latest close price to Google Sheets...")
    write_to_google_sheets(sheet_name, latest_close)
    print("Data written to Google Sheets successfully.")

    return latest_close  # Devolvemos el dato para que agente 2 lo pueda usar

if __name__ == "__main__":
    main()
