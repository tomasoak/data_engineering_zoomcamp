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
  -v "$(pwd)"/data/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5431:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

<br>

#### 2. Change folder permission
`sudo chmod a+rwx ny_taxi_postgres_data`

<br>

### 3. Install PostgreSQL CLI
<strong>Run the  command:</strong>
<br>
`sudo apt get pgcli`

<br>

<strong>Access database from the command line</strong>

`pgcli -h localhost -p 5431 -u root -d ny_taxi`

<br>

### 4. Automatically ingest into PostgreSQL - from python script
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

<br>

### Create a Postgres network
`docker network create pg-network`

<br>

### 5. Automatically ingest into PostgreSQL - from docker image that has the python ingestio script

URL="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-01.parquet"
URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
```
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

### 6. Install Terraform
https://developer.hashicorp.com/terraform/downloads
```
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install terraform
```

### 7. Install Google Cloud SK and login
https://cloud.google.com/sdk/docs/install#linux

### 7.a Create Service Account, Key and login
In Service account, add following roles: `Viewer`, `Storage Admin`, `Storage Object Admin`, `BigQuery Admin`

```
export GOOGLE_APPLICATION_CREDENTIALS="~/dataeng_zoomcamp/<xxxxx>.json"

gcloud auth application-default login
```

### 8. Running Terraform with GCP
run the following command in the same location `main.tf` and `variables.tf` files are located
```
terraform init
```

### 9. Run planning, which outputs Terraform is going to create or modify in our infrastructure (note that it will not apply anything, it just shows us what is going to be done if we decide to apply the changes). This command will ask us to inform the gcp project id variable.
```
terraform plan
```

### 10. Apply the changes.
```
terraform apply
```
The output of the terraform apply command must be something similar to:
```
google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 3s [id=projects/explorer-363509/datasets/trips_data_all]
google_storage_bucket.data-lake-bucket: Creation complete after 4s [id=dtc_data_lake_explorer-363509]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```


### 11. Add local SSH key to connect to GCP
```
cd ~/.ssh
ssh-keygen -t rsa -f gcp -C tomasoak -b 2048
```
Then
`cat gcp.pub`
and copy to `Metadata` on GCP