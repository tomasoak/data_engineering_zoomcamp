import os
from datetime import timedelta

import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash


@task(log_prints=True, retries=1, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract(url: str):
    os.system(f'wget {url} -O output.parquet')

    if url.endswith("parquet"):
        df = pd.read_parquet(url)
    elif url.endswith("csv"):
        df = pd.read_csv(url)

    return df


@task(log_prints=True)
def transform(df):
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df["passenger_count"] != 0]

    return df


@task(log_prints=True, retries=1)
def ingest(df, user, password, host, port, db):
    postgresql_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(postgresql_url)
    engine.connect()
    
    table_name = 'yellow_taxi_trips'

    df.to_sql(name=table_name, con=engine, if_exists="append")


@flow()
def main_flow():
    user = 'root'
    password = 'root'
    host = 'localhost'
    port = '5431'
    db = 'ny_taxi'
    
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

    raw_data = extract(url)
    data = transform(raw_data)
    ingest(data, user, password, host, port, db)
    

if __name__ == "__main__":
    main_flow()