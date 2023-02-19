<h1 align="center"> Instructions for Week 03 </h1>

<h2 align="center">Notes from the third week of the Data Engineering ZoomCamp</h2>

<br>
<br>
<br>

### Data Warehouse and BigQuery
1. OLAP x OLTP

OLTP - Online Transaction Processing:
<br>
- Captures, stores, and processes data from transactions in real time.

OLAP - Online Analytical Processing
- Uses complex queries to analyze aggregated historical data from OLTP systems.

<br>

2. What is Data Warehouse
It's an OLAP solution used for reporting and data analysis

<br>

### BigQuery
<br>
It's a servelss data warehouse
<br>
Provides scalability and high-availability
<br>
Built-in features like:
- machine learning
- geospatial analysis
- business intelligence

BigQuery Caches results
<br>
BiQuery Cost:
- On demand pricing: 1TB of data processed is $5
- Flate rate pricing: Based on number of pre requested slots - 100 slots -> $2,000/month / 400 TB data processed on demand pricing

<br>
Create table from csv on Google Storage:

```sql
CREATE OR REPLACE EXTERNAL TABLE `canvas-provider-xxxxxx.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://taxitrip_data/yellow_taxi_trip.csv'],
  field_delimiter  =';'
);
```
or from parquet file:
```sql
CREATE OR REPLACE EXTERNAL TABLE `canvas-provider-xxxxxx.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://taxitrip_data/yellow_taxi_trip.parquet'],
);
```
```sql
-- Closer look at partitions
SELECT table_name, partition_id, total_rows
FROM `taxi_trips.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_taxi_trip_partitioned'
ORDER BY total_rows DESC; 
```

### Partitioning and Clustering
```sql
CREATE OR REPLACE TABLE `canvas-provider-376717.taxi_trips.yellow_taxi_trip_partitioned_clustered`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM  `canvas-provider-376717.taxi_trips.yellow_taxi_trip`;
```

<br>

### BigQuery Partition
- Time-unit column
- Ingestion time (_PARTITIONTIME)
- Integer range partitioning
- When using Time unit or ingestion time:
  - Daily (default)
  - Hourly
  - Monthly or yearly
- Number of partitions limit is 4000

<br>

### BigQuery Clustering
- Order of the column is important
  - The order of the specified columns determines the sort order of the data
- Clustering improves:
  - Filter queries
  - Aggregate queries
- Can specify up to four clustering columns

<br>

### Clustering vs Partitioning
Clustering:
  - Cost benefit unknown
  - Need more granularity than partitioning alone allows
  - Multiple columns
Partitioning:
  - Cost known upfront
  - Need partition-level management
  - Filter or aggregate on single column

<br>

### Clustering over Partitioning
Use Cluster when:
- Partitioning results in a small amount of data per partition (< 1GB)
- Partitioning results in a large number of partitions beyond the limits (> 4000)
- Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (eg. every few minutes)

<br>

### BigQuery Best Practices
A. Cost reduction:
  - Price your queries before running them
  - Use clustered or partitioned tables
  - Use streaming inserts with caution
  - Materialize query results in stages

B. Query performance:
  - Filter on partitioned columns
  - Denormalizing data
  - Reduce data before using a `JOIN`
  - Do not treat `WITH` clauses as prepared statements
  - Avoid oversharding tables
  - Use approximate aggregation functions (eg. HyperLogLog++)
  - `ORDER` last
  - Place the table with largest number of rows first

<br>

### BigQuery Internals
[Ref link](https://panoply.io/data-warehouse-guide/bigquery-architecture/)

<br>

### ML in BigQuery
1. Create ML model, predict and evalute it
```SQL
-- CREATE A ML TABLE WITH APPROPRIATE TYPE
CREATE OR REPLACE TABLE `canvas-provider-376717.taxi_trips.yellow_taxi_trip_ml` (
  `passenger_count` INTEGER,
  `trip_distance` FLOAT64,
  `PULocationID` STRING,
  `DOLocationID` STRING,
  `payment_type` STRING,
  `fare_amount` FLOAT64,
  `tolls_amount` FLOAT64,
  `tip_amount` FLOAT64
  ) AS (
  SELECT CAST(passenger_count AS INTEGER), trip_distance, cast(PULocationID AS STRING), 
    CAST(DOLocationID AS STRING), CAST(payment_type AS STRING), fare_amount, tolls_amount, 
    tip_amount
  FROM `canvas-provider-376717.taxi_trips.yellow_taxi_trip_partitoned` WHERE fare_amount != 0
);


-- CREATE MODEL WITH DEFAULT SETTING
CREATE OR REPLACE MODEL `canvas-provider-376717.taxi_trips.tip_model`
OPTIONS
(model_type='linear_reg',
input_label_cols=['tip_amount'],
DATA_SPLIT_METHOD='AUTO_SPLIT') AS
SELECT * 
FROM `canvas-provider-376717.taxi_trips.yellow_taxi_trip_ml`
WHERE tip_amount IS NOT NULL;

-- CHECK FEATURES
SELECT * FROM ML.FEATURE_INFO(MODEL `canvas-provider-376717.taxi_trips.tip_model`);

-- EVALUATE THE MODEL
SELECT *
FROM ML.EVALUATE(MODEL `canvas-provider-376717.taxi_trips.tip_model`,
(SELECT *
  FROM `canvas-provider-376717.taxi_trips.yellow_taxi_trip_ml`
  WHERE tip_amount IS NOT NULL)
);

-- PREDICT AND EXPLAIN
SELECT *
FROM ML.EXPLAIN_PREDICT(MODEL `canvas-provider-376717.taxi_trips.tip_model`,
  (SELECT *
    FROM `canvas-provider-376717.taxi_trips.yellow_taxi_trip_ml`
    WHERE tip_amount IS NOT NULL),
  STRUCT(3 as top_k_features)
);

-- HYPER PARAM TUNNING
CREATE OR REPLACE MODEL `canvas-provider-376717.taxi_trips.tip_hyperparam_model`
OPTIONS
  (model_type='linear_reg',
  input_label_cols=['tip_amount'],
  DATA_SPLIT_METHOD='AUTO_SPLIT',
  num_trials=5,
  max_parallel_trials=2,
  l1_reg=hparam_range(0, 20),
  l2_reg=hparam_candidates([0, 0.1, 1, 10])) AS
    SELECT *
    FROM `canvas-provider-376717.taxi_trips.yellow_taxi_trip_ml`
    WHERE tip_amount IS NOT NULL;
```

2. ML Deployment 
Steps:
- gcloud auth login
```bash
bq --project_id taxi-rides-ny extract -m nytaxi.tip_model gs://taxi_ml_model/tip_model
mkdir /tmp/model
gsutil cp -r gs://taxi_ml_model/tip_model /tmp/model
mkdir -p serving_dir/tip_model/1
cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
docker pull tensorflow/serving
docker run -p 8501:8501 --mount type=bind,source=pwd/serving_dir/tip_model,target= /models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &
curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict
http://localhost:8501/v1/models/tip_model
```