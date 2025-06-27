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
        raise Exception(f"Error fetching data for {symbol}: {data.get('Note') or data.get('Error Message') or 'Unknown error'}")

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

def connect_to_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS_MULTI')
    if not creds_json:
        raise Exception("Google Sheets credentials not found in environment variables.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def write_dataframe_to_worksheet(spreadsheet, worksheet_name, df):
    try:
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")

        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f"✅ Data for {worksheet_name} updated in Google Sheets.")
    except Exception as e:
        print(f"⚠️ Error writing in tab '{worksheet_name}': {e}")

def main():
    print("🚀 Starting Agent 1 - Multi-symbol Ingestion")

    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not alpha_key:
        raise Exception("ALPHA_VANTAGE_API_KEY not found.")

    sheet_name = "Stocks"  
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"] 

    client = connect_to_sheets()
    spreadsheet = client.open(sheet_name)

    for symbol in symbols:
        print(f"📥Downloading data for: {symbol}")
        try:
            df = get_alpha_vantage_data(symbol, alpha_key)
            write_dataframe_to_worksheet(spreadsheet, symbol, df)
        except Exception as e:
            print(f"⚠️ Error  {symbol}: {e}")

if __name__ == "__main__":
    main()
