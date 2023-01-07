select count(*)
FROM {{ref('stock_data')}}
GROUP BY date, ticker
HAVING COUNT(*) > 1