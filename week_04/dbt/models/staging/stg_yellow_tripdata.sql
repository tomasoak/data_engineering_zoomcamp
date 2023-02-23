{{ config(materialized='view') }}

select *
from  {{ source('staging', 'yellow_taxi_trip_partitioned') }}
limit 10
