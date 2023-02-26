{{ config(materialized='view') }}

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, tpep_pickup_datetime) as rn
  from {{ source('staging', 'yellow_taxi_trip_partitoned') }}
  where vendorid is not null 
)
select 
  -- identifiers
  {{ dbt_utils.generate_surrogate_key(['vendorid']) }} as tripid,

  -- payment info
  cast(fare_amount as numeric) as fare_amount,
  cast(extra as numeric) as extra,
  {{ get_payment_type_description('payment_type') }} as payment_type_description, 
from tripdata
where rn = 1 
