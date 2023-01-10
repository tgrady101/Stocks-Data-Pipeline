{{ config(materialized='table') }}

select v.* , i.*, 
ROUND(((v.adjclose - LEAD(v.adjClose) OVER(PARTITION BY ticker ORDER BY date DESC)) / LEAD(v.adjClose) OVER(PARTITION BY ticker ORDER BY date DESC)) * 100, 2) as oneday_percent_change,
ROUND(((v.adjclose - LEAD(v.adjClose, 5) OVER(PARTITION BY ticker ORDER BY date DESC)) / LEAD(v.adjClose, 5) OVER(PARTITION BY ticker ORDER BY date DESC)) * 100, 2) as fiveday_percent_change,
ROUND(((v.adjclose - LEAD(v.adjClose, 20) OVER(PARTITION BY ticker ORDER BY date DESC)) / LEAD(v.adjClose, 20) OVER(PARTITION BY ticker ORDER BY date DESC)) * 100, 2) as twentyday_percent_change
FROM {{source('staging', 'stock_values')}} v
LEFT JOIN  {{source('staging', 'stock_info')}} i 
ON v.Ticker = i.Symbol