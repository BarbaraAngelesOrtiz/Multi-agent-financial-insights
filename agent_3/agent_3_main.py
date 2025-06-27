import os
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    if not creds_json:
        raise Exception("Google Sheets credentials not found in environment variables.")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def load_signals(sheet, tab_name):
    worksheet = sheet.worksheet(tab_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def analyze_signals(df):
    latest = df.iloc[-1]
    decision = "Keep"
    reasons = []

    if latest.get("buy1") == 1:
        reasons.append("EMA_10 > EMA_20 y RSI < 60")
    if latest.get("buy2") == 1:
        reasons.append("EMAs in an upward trend")

    if latest.get("sell1") == 1:
        reasons.append("RSI > 70 y close < EMA_10")
    if latest.get("sell2") == 1:
       reasons.append("RSI > 70 y close < EMA_20")

    if latest.get("buy1") or latest.get("buy2"):
        decision = "Buy"
    elif latest.get("sell1") or latest.get("sell2"):
        decision = "Sell"

    return decision, ", ".join(reasons), latest["Date"]

def write_recommendations(sheet, recommendations):
    try:
        try:
            ws = sheet.worksheet("Recommendations")
        except gspread.WorksheetNotFound:
            ws = sheet.add_worksheet(title=" Recommendations", rows="100", cols="10")
        df = pd.DataFrame(recommendations, columns=["Symbol", "Date", "Decision", "Reasons"])
        ws.clear()
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        print("✅ Updated recommendations.")
    except Exception as e:
        print(f"⚠️ Error writing recommendations: {e}")

def main():
    print("🚀 Starting Agent 3 - Signal Analysis")

    sheet_name = "Diary"
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]

    client = connect_to_google_sheets()
    sheet = client.open(sheet_name)

    recommendations = []

    for symbol in symbols:
        try:
            df = load_signals(sheet, symbol)
            decision, reasons, date = analyze_signals(df)
            recommendations.append([symbol, date, decision, reasons])
            print(f"📊 {symbol}: {decision} - {motivos}")
        except Exception as e:
            print(f"⚠️ Error  {symbol}: {e}")

    write_recommendations(sheet, recommendations)

if __name__ == "__main__":
    main()
