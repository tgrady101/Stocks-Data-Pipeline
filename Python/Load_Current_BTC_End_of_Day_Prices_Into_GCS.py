import pandas as pd
from google.cloud import storage, bigquery
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from tiingo import TiingoClient
import time
import pytz

def date_range():
    client = bigquery.Client(project='stocks-data-pipeline')
    job = client.query("""SELECT date
            FROM `stocks-data-pipeline.Stock_Info_Dataset.BTC_values`
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

def prepare_csv(beg_date, end_date):
    #Tiingo API Config
    config = {}
    config['session'] = True
    config['api_key'] = "0015ea3a0ed951cea8f45258393fd6b595327627"
    
    client = TiingoClient(config)
    historical_prices = client.get_crypto_price_history(tickers = ['BTCUSD'], startDate=beg_date, endDate=end_date, resampleFreq='24Hour')
    df = pd.DataFrame(historical_prices[0]["priceData"])
    df["ticker"] = "BTC"
    df['tradesDone'] = df['tradesDone'].astype(int)
    return df

def load_csv(df, ticker):
    #GCS Config
    today = datetime.now(pytz.timezone('US/Eastern'))
    today = today.strftime('%Y-%m-%d')
    client = storage.Client()
    bucket = client.get_bucket('data_lake_stocks-data-pipeline')
    bucket.blob(f'{ticker} Updated Data as of {today}').upload_from_string(df.to_csv(), "BTC Updated Price Data")
    
def main():
    beg_date, end_date = date_range()
    csv = prepare_csv(beg_date, end_date)
    load_csv(csv, "BTC")

if __name__ == "__main__":
    main()
        
        
