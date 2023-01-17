import pyspark
from pyspark.sql import SparkSession, types
from google.cloud import bigquery


def transform_df(spark):

    schema = types.StructType([
    types.StructField('_c0', types.StringType(), True),
    types.StructField('Symbol', types.StringType(), True),
    types.StructField('Security', types.StringType(), True), 
    types.StructField('SEC_Fillings', types.StringType(), True),
    types.StructField('GICS_Sector', types.StringType(), True), 
    types.StructField('GICS_Sub_Industry', types.StringType(), True), 
    types.StructField('Headquarters_Location', types.StringType(), True), 
    types.StructField('Date_First_Added', types.DateType(), True), 
    types.StructField('CIK', types.IntegerType(), True), 
    types.StructField('Founded', types.StringType(), True), 
    ])

    bucket_name="data_lake_stocks-data-pipeline"
    path=f"gs://{bucket_name}/S&P 500 Company Info"
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
    BQ_TABLE = "stock_info"

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
    df = transform_df(spark)
    load_df(df)

if __name__ == "__main__":
    main()
