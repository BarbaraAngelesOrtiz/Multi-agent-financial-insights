import os
import json
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_alpha_vantage_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise Exception("Error fetching data from Alpha Vantage.")

    time_series = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index.name = "Date"
    df.reset_index(inplace=True)
    df.sort_values(by="Date", ascending=False, inplace=True)
    return df

def write_to_google_sheets(sheet_name, dataframe):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    if not creds_json:
        raise Exception("Google Sheets credentials not found in environment variables.")

    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(sheet_name).worksheet('Sheet1')

    except gspread.SpreadsheetNotFound:
        raise Exception(f"Spreadsheet with name '{sheet_name}' not found. Check the title and permissions.")

    # Limpiar y escribir encabezados + datos
    sheet.clear()
    sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

def main():
    print("Starting Agent 1 - Data Ingestion...")

    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not alpha_key:
        raise Exception("Alpha Vantage API key not found in environment variables.")

    symbol = "AAPL"
    print(f"Fetching data for {symbol}...")
    df = get_alpha_vantage_data(symbol, alpha_key)
    

