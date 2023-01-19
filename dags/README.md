![](https://github.com/tgrady101/Stocks-Data-Pipeline/blob/main/BTC%20DAG.png)
![](https://github.com/tgrady101/Stocks-Data-Pipeline/blob/main/Stock%20DAG.png)
One DAG uploads all the missing S&P 500 end of day values to GCS, moves the data from GCS to BigQuery, then runs dbt transformations<br>
The second DAG does the same process but for BTC price data
