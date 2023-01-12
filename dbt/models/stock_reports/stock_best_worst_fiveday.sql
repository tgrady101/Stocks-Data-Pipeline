{{ config(materialized="table") }}

--Use LEAD function to pull close from one/five/twenty trading days ago. Use to calculate return percentage over that period.
--Pull top five and bottom five values along with SPY as a reference

(select *
from {{ ref("stock_data") }}
WHERE date = CURRENT_DATE('EST5EDT') AND fiveday_percent_change IS NOT NULL
order by fiveday_percent_change asc
limit 5)

UNION ALL

(select *
from {{ ref("stock_data") }}
WHERE date = CURRENT_DATE('EST5EDT') AND fiveday_percent_change IS NOT NULL
order by fiveday_percent_change desc
limit 5)
