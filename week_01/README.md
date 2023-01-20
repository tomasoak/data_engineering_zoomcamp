<h1 align="center"> Instructions for Week 01 </h1>

<h2 align="center">Notes from the first week of the Data Engineering ZoomCamp</h2>

<br>
<br>
<br>

### 1. Create a PostgreSQL (v.13) image with database `ny_taxi`
<strong>Run the  command:</strong>
```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "$(pwd)"/week_01/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5431:5432 \
  postgres:13
```

<br>

### 2. Install PostgreSQL CLI
<strong>Run the  command:</strong>
<br>
`sudo apt get pgcli`

<br>

<strong>Access database from the command line</strong>

`pgcli -h localhost -p 5431 -u root -d ny_taxi`

<br>

### 3. Automatically ingest into PostgreSQL
Instead of downloading the NYC Taxi Data it's possible to ingest it automatically into the database with the following commands

```
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet" 

python ingest_data.py \
--user=root \
--password=root \
--host=localhost \
--port=5431 \
--db=ny_taxi \
--table_name=yellow_taxi_trips \
--url=${URL}
```