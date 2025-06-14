# Multi-Agent Financial Insights System 🧠📊

This project is part of the **Google Cloud Multi-Agent Hackathon**, under the category:

> **Data Analysis and Insights:** Create multi-agent systems that autonomously analyze data from various sources, derive meaningful insights using tools like BigQuery, and collaboratively present findings.

## 🚀 Overview

We built a 3-agent system that automates the full data analysis pipeline for financial stock data — from data ingestion to insight generation and visualization — using the power of Google Cloud and Python.

### 👩‍💻 Author
**Bárbara Ángeles Ortiz**  
Electrical & Data Engineer | Satellite Hackathon Enthusiast  
🇦🇷 Based in Ireland  
[LinkedIn](https://www.linkedin.com/in/barbaraangelesortiz/) | [GitHub](https://github.com/BarbaraAngelesOrtiz)

---

## 🧠 System Architecture

| Agent # | Role | Description |
|--------|------|-------------|
| **Agent 1** | 🟢 Data Ingestion Agent | Fetches stock data from Alpha Vantage, formats it, and stores in Google Sheets and/or BigQuery. |
| **Agent 2** | 🟡 BigQuery Analysis Agent | Loads financial data from BigQuery, performs statistical analysis, trend detection and indicator extraction (SMA, RSI, etc.). |
| **Agent 3** | 🔵 Insight Presenter Agent | Summarizes the findings, generates plain-language insights and graphs, and can export a PDF/Markdown report or feed a Google Chat bot. |

---

## 📂 Project Structure

