from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
  """Read taxi data from web into pandas DataFrame"""
  # if randint(0,1) > 0 :
  #   raise Exception

  df = pd.read_parquet(dataset_url)
  print(f"rows: {len(df)}")
  return df

@task(log_prints=True)
def transform(df = pd.DataFrame) -> pd.DataFrame:
  """Fix data type"""
  df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
  df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
  
  return df


@task()
def write_local(df) -> Path:
  """Write DataFrame out locally as a csv file"""
  # Path.mkdir("data")
  path = Path(f"yellow_taxi_trip.parquet")
  df.to_parquet(path)
  # df.head(100).to_csv("yellow_taxi_trip.csv", index=False, sep=";")

  return path


@task()
def write_gcs(path: Path) -> None:
  """Upload parquet file to Google Cloud Storage"""

  gcp_block = GcsBucket.load("taxitrip-data")
  gcp_block.upload_from_path(
    from_path = path,
    to_path = path
  )

  return 


@flow()
def etl_web_to_gcp() -> None:
  """Main ETL function"""
  dataset_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet" 

  df = fetch(dataset_url)
  df = transform(df)
  path = write_local(df)
  write_gcs(path)

  return df

if __name__ == "__main__":
  etl_web_to_gcp()