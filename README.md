# Multi-Agent Stock Signal System 📊

This project uses automated agents to download, analyze, and recommend stock signals in real time, integrated with Google Sheets and scheduled to run daily using GitHub Actions.

-----

## 🚀 Overview

I built a 3-agent system that automates the full data analysis pipeline for financial stock data, from data ingestion to insight generation and visualization, using the power of Google Cloud and Python.

-----

## 🧠 System Agents

| Agent # | Role | Description |
|--------|------|-------------|
| **Agent 1** | 🟢 Data Ingestion Agent | Fetches stock data from Alpha Vantage, formats it, and stores in Google Sheets and/or BigQuery. |
| **Agent 2** | 🟡 BigQuery Analysis Agent | Loads financial data from BigQuery, performs statistical analysis, trend detection and indicator extraction (SMA, RSI, etc.). |
| **Agent 3** | 🔵 Insight Presenter Agent | Summarizes the findings, generates plain-language insights and graphs, and can export a PDF/Markdown report or feed a Google Chat bot. |

-----

## 📂 Project Structure

### 🛰️ Agent 1 - Data Ingestion
Automatically downloads daily historical stock data using the [Alpha Vantage](https://www.alphavantage.co/) API and saves it to Google Sheets spreadsheets (one tab per symbol).

- 📥 Source: Alpha Vantage (TIME_SERIES_DAILY)
- 📝 Destination: Google Sheets (`Diary` → `AAPL`, `GOOGL`, etc.)
- ⏱️ Frequency: Every day at 7:00 PM UTC (cron job)

-----

#### Required Variables
- `ALPHA_VANTAGE_API_KEY` (in **GitHub Secrets**)
- `GOOGLE_SHEETS_CREDENTIALS` (JSON from the service account in **GitHub Secrets**)

-----

### 🚦 Agent 2 - Signal Calculation *(optional, if implemented)*

Calculates technical indicators such as:
- RSI
- EMAs (10, 20, etc.)
- Boolean signals: `buy1`, `buy2`, `sell1`, `sell2`, ​​etc.

Updates each sheet (`AAPL`, `GOOGL`, etc.) with the new columns.

-----

### 🤖 Agent 3 - Signal Analysis & Recommendation

Reads technical signals from each individual sheet and generates a recommendation table in a special tab.

- 📊 Analyzes: RSI, EMAs, and buy/sell conditions
- 📄 Writes: `Recommendations` sheet in Google Sheets
- 💡 Output: Symbol | Date | Decision | Reasons

Example:
| Symbol | Date | Decision | Reasons |
|---------|-------------|----------|----------------------------------------|
| AAPL | 2025-06-27 | Buy | EMA_10 > EMA_20 and RSI < 60 |
| MSFT | 2025-06-27 | Sell | RSI > 70 and price < EMA_20 |

-----

## Author
**Bárbara Ángeles Ortiz**

<img src="https://github.com/user-attachments/assets/30ea0d40-a7a9-4b19-a835-c474b5cc50fb" width="115">

[LinkedIn](https://www.linkedin.com/in/barbaraangelesortiz/) | [GitHub](https://github.com/BarbaraAngelesOrtiz)

![Status](https://img.shields.io/badge/status-finished-brightgreen) 📅 July 2025

![Python](https://img.shields.io/badge/python-3.10-blue)

![NumPy](https://img.shields.io/badge/numpy-1.26.0-blue)

![Pandas](https://img.shields.io/badge/pandas-2.1.0-blue)

![GitHub Actions](https://img.shields.io/badge/build-passing-brightgreen)



