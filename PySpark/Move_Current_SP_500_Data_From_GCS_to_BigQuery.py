import pyspark
from pyspark.sql import SparkSession, types
from google.cloud import bigquery
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timezone
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

def transform_df(ticker, spark):

    schema = types.StructType([
    types.StructField('_c0', types.StringType(), True),
    types.StructField('date', types.DateType(), True), 
    types.StructField('close', types.FloatType(), True), 
    types.StructField('high', types.FloatType(), True), 
    types.StructField('low', types.FloatType(), True), 
    types.StructField('open', types.FloatType(), True), 
    types.StructField('volume', types.IntegerType(), True), 
    types.StructField('adjClose', types.FloatType(), True), 
    types.StructField('adjHigh', types.FloatType(), True), 
    types.StructField('adjLow', types.FloatType(), True),
    types.StructField('adjOpen', types.FloatType(), True),
    types.StructField('adjVolume', types.IntegerType(), True), 
    types.StructField('divCash', types.FloatType(), True), 
    types.StructField('splitFactor', types.FloatType(), True), 
    types.StructField('ticker', types.StringType(), True), 
    ])

    bucket_name="data_lake_stocks-data-pipeline"
    today = datetime.now(pytz.timezone('US/Eastern'))
    today = today.strftime('%Y-%m-%d')
    path=f"gs://{bucket_name}/{ticker} Updated Data as of {today}"
    df = spark.read \
        .option('header', 'true') \
        .schema(schema) \
        .csv(path)
    df = df.drop('_c0')
    return df

def load_df(df):
    #Load Data to BigQuery Table
    GCP_PROJECT_ID = "stocks-data-pipeline"
    BQ_DATASET = "Stock_Info_Dataset"
    BQ_TABLE = "stock_values"

    df.write \
        .format('bigquery') \
        .option("temporaryGcsBucket", "dataproc-temp-us-central1-230775253-kdxhumag") \
        .mode("append") \
        .option('table', f'{GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}') \
        .save()

def main():
    #Setup Spark Session
    spark = SparkSession \
        .builder \
        .master('yarn') \
        .appName('test') \
        .getOrCreate()
    ticker_list = gen_ticker_list()
    for ticker in ticker_list:
        df = transform_df(ticker, spark)
        load_df(df)

if __name__ == "__main__":
    main()
