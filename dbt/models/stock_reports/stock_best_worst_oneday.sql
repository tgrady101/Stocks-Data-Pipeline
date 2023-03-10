{{ config(materialized="table") }}

--Pull top five and bottom five values along with SPY as a reference

(select *
from {{ ref("stock_data") }}
WHERE date =  CURRENT_DATE('EST5EDT') AND oneday_percent_change IS NOT NULL
order by oneday_percent_change asc
limit 5)

UNION ALL

(select *
from {{ ref("stock_data") }}
WHERE date = CURRENT_DATE('EST5EDT') AND oneday_percent_change IS NOT NULL
order by oneday_percent_change desc
limit 5)

