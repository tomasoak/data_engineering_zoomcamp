{{ config(materialized='view') }}

select *
from public.green_taxi_trip -- OR {{ source('staging', 'yellow_taxi_trip') }}
