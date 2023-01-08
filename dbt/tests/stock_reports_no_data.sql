--Check if no records are returned for the stock report. Useful for weekday holidays with no trading data.

SELECT date,
    CASE WHEN date != CURRENT_DATE('EST5EDT') 
    THEN 'No Current Stock Data'
    END AS result
    FROM {{ref('stock_data')}}
    ORDER BY DATE DESC
    LIMIT 1