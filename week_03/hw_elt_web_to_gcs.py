"""
Exercise - ELT from web to BigQuery
"""

import os
import requests
from pathlib import Path

from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3, log_prints=True)
def extract() -> None:
  url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_"
      
  def download_raw_data(url: str, year: int, month: int):
    raw_data = requests.get(f"{url}{year}-{month:02}.csv.gz", stream=True)

    with open(f"data/fvh_tripdata_{year}-{month:02}.csv.gz", 'wb') as f:
      for chunk in raw_data.raw.stream(1024, decode_content=False):
          if chunk:
            f.write(chunk)

  for year in range(2019, 2022):
    if year == 2021:
      for month in range(1,2):
        download_raw_data(url, year, month)
    else:
      for month in range(1, 13):
        download_raw_data(url, year, month)


# asyncio.exceptions.CancelledError
@task(retries=3, log_prints=True, timeout_seconds=60) 
def load_gcs() -> None:
  """Load files to Google Cloud Storage"""

  gcp_block = GcsBucket.load("fhv-trip-data")

  for files in os.walk("data/"):
    for file in files:
      for i in file:
        if i.endswith("csv.gz"):
          file_path = os.path.join(Path(), f"data/{i}")
    
          gcp_block.upload_from_path(
              from_path = file_path,
              to_path = i
          )


@flow(name="ELT web to GCS")
def elt_web_to_gcs():
  extract()
  load_gcs()


if __name__ == "__main__":
  elt_web_to_gcs()