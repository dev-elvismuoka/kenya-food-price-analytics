/* This model cleans the raw maize and beans data.
   We call it a 'dim' (dimension) table because it holds 
   descriptive data about food prices.
*/

WITH raw_data AS (
    SELECT 
        date::DATE as price_date,
        UPPER(market_name) as market_location, -- Standardize to uppercase
        LOWER(commodity_name) as commodity,
        price::DECIMAL(10,2) as price_kes,
        ingested_at
    FROM {{ source('public', 'raw_food_prices') }}
    WHERE price IS NOT NULL
)

SELECT * FROM raw_data