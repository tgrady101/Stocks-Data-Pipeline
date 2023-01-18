# Summary

This project involved creating a data pipeline to analyze S&P 500 end of day prices going from three years ago to the current day. The data is processed via an ETL pipeline that supports a dashboard which shows the top five and bottom five stocks over different historical periods.

# Tools and Technologies Used

* Cloud — Google Cloud Platform
* Infrastructure as Code — Terraform
* Containerization — Docker, Docker Compose
* Orchestration — Airflow
* Transformation — Spark
* Transformation — dbt
* Data Lake — Google Cloud Storage
* Data Warehouse — BigQuery
* Data Visualization — Tableau
* Languages — Python, SQL
* Operating System — Linux (Ubuntu)
* Version Control — Git

# Architecture

I started by creating a Ubuntu virtual machine on the Google cloud to run everything. I used Terraform to setup a GCS data lake and a BigQuery data warehouse with several associated tables. I used python/Beautiful Soup/pandas to scrape the Wiki page that has an up to date list of S&P 500 companies to generate a list of tickers along with pulling some information about the different companies. I ran that list through the API associated with a financial reporting service called Tiingo to read three years of historical end of day prices for S&P 500 companies.

To transfer the data from GCS to BigQuery I used PySpark. I loaded the data from GCS into a PySpark dataframe, made some minor transformations, and then wrote the data to the relevant BigQuery tables. I also created python scripts to load current data to GCS based on the latest data already in BigQuery with the intention of adding fresh data every day (but also with the ability to catch up if a day was missed). I added PySpark scripts to move the current data to BigQuery.

# Orchestration

I used Apache Airflow to automate all of my daily data processes and ran it via a Docker container. I created a DAG to automatically upload data to GCS, move data to BigQuery via PySpark, and then transform data via dbt. The DAG was scheduled to run every weekday.


# Transformation

While I performed a few small transformations via PySpark most of the transformations were done with dbt using SQL. Data about the S&P 500 companies and end of day price data is joined into a staging table. After that new report tables are generated to show the top five and bottom five stocks over one/five/twenty trading day periods. The report tables are overwritten every weekday as new data is loaded. Changes to my queries are made in a testing branch and then pushed to the main branch once I confirm there are no errors.

# Testing

Inside of my dbt schema.yml file I use the default not_null and unique tests on a variety of fields to test the data for issues. I also have a custom test defined to check if the last date in my BigQuery data isn’t today indicating it is a trading holiday and the report tables don’t need to updated.


# Dashboard

Once the dbt job is run my final result is a Tableau dashboard updated to the current days data. The dashboard shows the top five and bottom five S&P 500 stocks over the last one/five/twenty trading days.

# Next Steps

My next goal is to create a similar data pipeline but streaming real time data via Kafka.

