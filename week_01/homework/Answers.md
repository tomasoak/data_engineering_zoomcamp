<h1 align="center">Homework assignment week 01</h1>

## Question 1.
`docker build --help`

<br>

## Question 2.
```
docker run -it --entrypoint=bash python:3.9
pip list
```

<br>

## Question 3.
Ingest script can be checked [HERE](https://github.com/tomasoak/dataeng_zoomcamp/blob/main/week_01/ingest_data.py)

Ingest `green_tripdata` data into PostgreSQL
<br>

```
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-01.parquet"
docker run -it \
  --network=pg-network \
  taxi_ingest_v01 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432\
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --url=${URL}
```
<br>

Ingest `taxi_zone` data into PostgreSQL

```
URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
docker run -it \
  --network=pg-network \
  taxi_ingest_v01 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432\
    --db=ny_taxi \
    --table_name=taxi_zone \
    --url=${URL}
```

```
-- Query
SELECT COUNT(1)
FROM public.green_taxi_trips
WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-01-15' AND CAST(lpep_dropoff_datetime AS DATE) = '2019-01-15'
```

<br>

## Question 4.
```
SELECT CAST(lpep_dropoff_datetime AS DATE), SUM(trip_distance) trip_distance
FROM public.green_taxi_trips
GROUP BY CAST(lpep_dropoff_datetime AS DATE)
ORDER BY 2 desc
```
<br>

## Question 5.

<br>

## Question 6.

<br>

## Learning in public links
[Start](https://www.linkedin.com/feed/update/urn:li:activity:7020835983008903168/)