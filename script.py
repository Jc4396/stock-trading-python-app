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
    time.sleep(30)  # 5 requests per minute

print(len(tickers))
