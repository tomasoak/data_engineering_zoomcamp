<h1 align="center"> Instructions for Week 01 </h1>

<h2 align="center">Notes from the first week of the Data Engineering ZoomCamp</h2>

<br>
<br>
<br>

### 1. Create a PostgreSQL (v.13) image with database `ny_taxi`
<strong>Run the  command:</strong>
```bash
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

```bash
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
```bash
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

<br>

### 6. Install Terraform
https://developer.hashicorp.com/terraform/downloads
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install terraform
```

<br>

### 7. Install Google Cloud SK and login
https://cloud.google.com/sdk/docs/install#linux

### 7.a Create Service Account, Key and login
In Service account, add following roles: `Viewer`, `Storage Admin`, `Storage Object Admin`, `BigQuery Admin`

```bash
export GOOGLE_APPLICATION_CREDENTIALS="~/dataeng_zoomcamp/<xxxxx>.json"

gcloud auth application-default login
```

<br>

### 8. Running Terraform with GCP
run the following command in the same location `main.tf` and `variables.tf` files are located
```bash
terraform init
```

<br>

### 9. Run planning, which outputs Terraform is going to create or modify in our infrastructure (note that it will not apply anything, it just shows us what is going to be done if we decide to apply the changes). This command will ask us to inform the gcp project id variable.
```bash
terraform plan
```

<br>

### 10. Apply the changes.
```bash
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
<br>

___
## Replicating above steps in a GCP VM 

<br>

### 11. Add local SSH key to connect to GCP
```bash
cd ~/.ssh
ssh-keygen -t rsa -f gcp -C tomasoak -b 2048
```
Then
`cat gcp.pub`
and copy to `Metadata` on GCP

<br>

### 12. Create VM machine
- Machine type: `e2-standard-4 (4 vCPU, 16 GB Memory)`
- Image: Ubutu 20.04 LTS 

<br>

### 13. Connect local env to VM via ssh
ssh -i ~/.ssh/<private_key> <name_used>@<VM_external_IP>

```bash
cd ~
ssh -i ~/.ssh/gcp tomasoak@34.88.193.200
```
<br>

### 14. Create config file
```bash
cd ~/.ssh
touch config
vim config
```
Inside config insert:
```
Host de-zoomcamp
  HostName 34.88.193.200 <check VM's external IP - it's changing dynamically>
  User tomasoak
  IdentityFile /home/tomasoak/.ssh/gcp
```
Then it's possible to access the VM with the command: `ssh de-zoomcamp`

<br>

### 15. Install Anaconda inside VM
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh 
```

<br>

### 16. Update apt and install docker
```bash
sudo apt-get update
sudo apt install docker.io
```

<br>

### 17. Clone course repo
```
git clone https://github.com/tomasoak/dataeng_zoomcamp.git
```

<br>

### 18. Docker without sudo 
```bash
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
```

<br>

### 19. Install Docker-Compose
```bash
mkdir bin
cd bin/
wget https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -O docker-compose
chmod +x docker-compose
```

<br>

### 20. Add shortcut to docker-compose
```bash
nano .bashrc
```

in the end add:

```bash
export PATH="{$HOME}/bin:${PATH}"
```
press CTRL+O and Enter -> to save
<br>
press CTRL+X to quit

<br>

### 21. Download postgres image
```bash
cd dataeng_zoomcamp/week_01
docker-compose up -d
```

<br>

### 22. Install pgcli
```bash
pip install pgcli
pgcli -h localhost -U root -d ny_taxi 
```

### 23. Install Terraform
```bash
wget https://releases.hashicorp.com/terraform/1.3.7/terraform_1.3.7_linux_amd64.zip
sudo apt install unzip
unzip terraform_1.3.7_linux_amd64.zip
```

### 24. Export GCP Credentials and authenticate
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/gcp_credentials.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

### 25. Terraform
```bash
cd dataeng_zoomcamp/week_01/terraform
terraform init
terraform plan
terraform apply
```

### 26. Shutdown
```bash
sudo shutdown now
```