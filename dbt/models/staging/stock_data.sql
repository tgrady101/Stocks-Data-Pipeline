{{ config(materialized='table') }}

select v.* , i.*, 
((v.adjclose - LEAD(v.adjClose) OVER(PARTITION BY ticker ORDER BY date DESC)) / LEAD(v.adjClose) OVER(PARTITION BY ticker ORDER BY date DESC)) as oneday_percent_change,
((v.adjclose - LEAD(v.adjClose, 5) OVER(PARTITION BY ticker ORDER BY date DESC)) / LEAD(v.adjClose, 5) OVER(PARTITION BY ticker ORDER BY date DESC)) as fiveday_percent_change,
((v.adjclose - LEAD(v.adjClose, 20) OVER(PARTITION BY ticker ORDER BY date DESC)) / LEAD(v.adjClose, 20) OVER(PARTITION BY ticker ORDER BY date DESC)) as twentyday_percent_change
FROM {{source('staging', 'stock_values')}} v
LEFT JOIN  {{source('staging', 'stock_info')}} i 
ON v.Ticker = i.Symbol