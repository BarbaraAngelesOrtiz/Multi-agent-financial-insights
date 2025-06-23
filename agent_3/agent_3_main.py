import os
import json
import gspread
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()


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
    ema20 = l
