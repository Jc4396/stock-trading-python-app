import csv
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

LIMIT = 1000

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"
response = requests.get(url)
tickers = []

data = response.json()
for ticker in data["results"]:
    tickers.append(ticker)

while "next_url" in data:
    response = requests.get(data["next_url"] + f"&apiKey={POLYGON_API_KEY}")
    data = response.json()
    print(data)
    for ticker in data["results"]:
        tickers.append(ticker)
    time.sleep(15)  # 5 requests per minute

example_ticker = {
    "ticker": "ZTAX",
    "name": "X-Square Municipal Income ETF",
    "market": "stocks",
    "locale": "us",
    "primary_exchange": "ARCX",
    "type": "ETF",
    "active": True,
    "currency_name": "usd",
    "composite_figi": "BBG01GQV0TJ2",
    "share_class_figi": "BBG01GQV0VC4",
    "last_updated_utc": "2025-10-01T06:06:06.417975318Z",
}


# Write tickers to csv with example_ticker schema
fieldnames = list(example_ticker.keys())
output_csv = "tickers.csv"
with open(output_csv, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:
        row = {key: t.get(key, "") for key in fieldnames}
        writer.writerow(row)
print(f"Wrote {len(tickers)} tickers to {output_csv}")
