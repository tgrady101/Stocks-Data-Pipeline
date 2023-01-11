#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import storage, bigquery
from datetime import datetime, timedelta, timezone
from tiingo import TiingoClient
import time
import pytz

def gen_ticker_list():
    page = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks")
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table')
    df = pd.read_html(str(table))[0]
    temp_list = df["Symbol"].tolist()
    ticker_list = []
    for i in temp_list:
        temp = i.replace(".","-")
        ticker_list.append(temp)
    ticker_list.append('SPY')
    return ticker_list

def date_range(ticker):
    client = bigquery.Client(project='stocks-data-pipeline')
    job = client.query(f"""SELECT date
            FROM `stocks-data-pipeline.Stock_Info_Dataset.stock_values`
            WHERE Ticker = '{ticker}'
            ORDER BY date DESC
            LIMIT 1""")
    for row in job.result():
        temp_date = format(row[0])
    beg_date = datetime.strptime(temp_date, "%Y-%m-%d")
    beg_date = beg_date + timedelta(days = 1)
    beg_date = beg_date.astimezone(pytz.timezone('US/Eastern'))
    end_date = datetime.now(pytz.timezone('US/Eastern'))
    assert beg_date <= end_date, "Beginning Date is in the Future"
    beg_date = beg_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return beg_date, end_date

 
def prepare_csv(ticker, beg_date, end_date):
    #Tiingo API Config
    config = {}
    config['session'] = True
    config['api_key'] = "0015ea3a0ed951cea8f45258393fd6b595327627"
    client = TiingoClient(config)
    historical_prices = client.get_ticker_price(ticker, fmt='json', startDate=beg_date, endDate=end_date, frequency='daily')
    df = pd.DataFrame(historical_prices)
    df["ticker"] = ticker
    return df

def load_csv(df, ticker):
    #GCS Config
    today = datetime.now(pytz.timezone('US/Eastern'))
    today = today.strftime('%Y-%m-%d')
    client = storage.Client()
    bucket = client.get_bucket('data_lake_stocks-data-pipeline')
    bucket.blob(f'{ticker} Updated Data as of {today}').upload_from_string(df.to_csv(), "S&P 500 Updated Daily Prices")

def main():
    ticker_list = gen_ticker_list()
    for ticker in ticker_list:
        beg_date, end_date = date_range(ticker)
        df = prepare_csv(ticker, beg_date, end_date)
        load_csv(df, ticker)
        time.sleep(1)
    
if __name__ == "__main__":
    main()
    
