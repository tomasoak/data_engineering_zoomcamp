from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs() -> Path:
  """Download trip data from GCS"""

  gcs_path = "yellow_taxi_trip.parquet"
  gcs_block = GcsBucket.load("taxitrip-data")
  gcs_block.get_directory(from_path=gcs_path, local_path="data/")

  return Path(f"data/{gcs_path}")


@task(log_prints=True)
def transform(path):
  df = pd.read_parquet(path)
  print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
  df["passenger_count"] = df["passenger_count"].fillna(0)
  print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")

  return df

@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
  """Write DataFrame to BigQuery"""

  gcp_credentials_block = GcpCredentials.load("zoom-gcp")

  df.to_gbq(
    destination_table="taxitripparquet.rides",
    project_id="canvas-provider-376717",
    credentials=gcp_credentials_block.get_credentials_from_service_account(),
    chunksize=500_000,
    if_exists="append"
  )



@flow()
def etl_gcs_to_bq():
  """Main ETL flow to load data from Google Cloud Storage to BigQuery"""

  path = extract_from_gcs()
  df = transform(path)
  write_bq(df)


if __name__ == "__main__":
  etl_gcs_to_bq()