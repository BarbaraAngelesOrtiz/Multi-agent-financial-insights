import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_alpha_vantage_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def write_to_google_sheets(sheet_name, data):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_CREDS_JSON')
    if not creds_json:
        raise Exception("Google credentials JSON not found in environment variables.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1

    # Aquí agregas tu lógica para escribir datos
    sheet.update('A1', 'Datos actualizados')

def main():
    print("Starting script...")

    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not alpha_key:
        raise Exception("Alpha Vantage API key not found in environment variables.")

    symbol = 'AAPL'  # ejemplo

    print(f"Fetching data for {symbol} from Alpha Vantage...")
    data = get_alpha_vantage_data(symbol, alpha_key)
    print("Data fetched successfully.")

    print("Writing data to Google Sheets...")
    write_to_google_sheets('Your Google Sheet Name', data)
    print("Data written to Google Sheets successfully.")

if __name__ == "__main__":
    main()
