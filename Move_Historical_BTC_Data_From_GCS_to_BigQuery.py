import pyspark
from pyspark.sql import SparkSession, types
from google.cloud import bigquery

#Create pyspark dataframe based on .csv data in GCS
def transform_df(ticker, spark):

    #Setup pyspark schema
    schema = types.StructType([
    types.StructField('_c0', types.StringType(), True),
    types.StructField('date', types.DateType(), True),
    types.StructField('open', types.FloatType(), True), 
    types.StructField('high', types.FloatType(), True),
    types.StructField('low', types.FloatType(), True), 
    types.StructField('close', types.FloatType(), True), 
    types.StructField('volume', types.FloatType(), True), 
    types.StructField('volumeNotional', types.FloatType(), True), 
    types.StructField('tradesDone', types.IntegerType(), True), 
    types.StructField('ticker', types.StringType(), True), 
    ])

    #Read data from GCS
    bucket_name="data_lake_stocks-data-pipeline"
    path=f"gs://{bucket_name}/{ticker} Three Year Daily Price History"
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
    BQ_TABLE = "BTC_values"

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
    ticker = "BTC"
     #Create pyspark dataframe
    df = transform_df(ticker, spark)
    #load to BigQuery
    load_df(df)

if __name__ == "__main__":
    main()