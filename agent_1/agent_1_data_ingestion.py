import os
import json
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_alpha_vantage_data(symbol: str, api_key: str) -> pd.DataFrame:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&datatype=json&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'Time Series (Daily)' not in data:
        raise Exception(f"Error fetching data for {symbol}: {data.get('Note') or data.get('Error Message') or 'Unknown error'}")

    ts_data = data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(ts_data, orient='index').sort_index()
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index.name = 'Date'
    df.reset_index(inplace=True)
    return df

def write_to_google_sheets(sheet_name: str, df: pd.DataFrame):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    if not creds_json:
        raise Exception("Google credentials JSON not found in environment variables.")
    
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    sheet.clear()
    
    # Escribimos encabezados y datos
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

def main():
    print("Starting Agent 1 - Data Ingestion...")

    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not alpha_key:
        raise Exception("Alpha Vantage API key not found in environment variables.")

    symbol = 'AAPL'  # Cambia o hazlo dinámico si quieres varios
    sheet_name = 'Financial Data'  # Debe existir en tu Google Drive

    print(f"Fetching data for {symbol}...")
    df = get_alpha_vantage_data(symbol, alpha_key)
    print("Data fetched successfully.")

    print("Writing data to Google Sheets...")
    write_to_google_sheets(sheet_name, df)
    print("Data written successfully.")

if __name__ == "__main__":
    main()
