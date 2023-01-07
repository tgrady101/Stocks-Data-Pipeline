{{ config(materialized='table') }}

--Use LEAD function to pull close from one/five/twenty trading days ago. Use to calculate return percentage over that period.
select *, 
ROUND(((close - LEAD(close) OVER(ORDER BY date DESC)) / LEAD(close) OVER(ORDER BY date DESC)) * 100, 2) as oneday_percent_change,
ROUND(((close - LEAD(close, 5) OVER(ORDER BY date DESC)) / LEAD(close, 5) OVER(ORDER BY date DESC)) * 100, 2) as fiveday_percent_change,
ROUND(((close - LEAD(close, 20) OVER(ORDER BY date DESC)) / LEAD(close, 20) OVER(ORDER BY date DESC)) * 100, 2) as twentyday_percent_change
FROM {{source('staging', 'BTC_values')}} 
WHERE date = CURRENT_DATE('EST5EDT')
