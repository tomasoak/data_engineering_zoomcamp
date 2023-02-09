import os
from datetime import timedelta
import argparse

import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash

from prefect_sqlalchemy import SqlAlchemyConnector


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
def ingest(df, table_name):
    connection_block = SqlAlchemyConnector.load("pg-local")

    with connection_block.get_connection(begin=False) as engine:
        df.to_sql(name=table_name, con=engine, if_exists="append")


@flow(name="Sub-flow", log_prints=True)
def log_subflow(table_name: str):
    print(f"Logging Subflow for: {table_name}")
    

@flow()
def main_flow(params):
    table_name = params.table_name
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

    log_subflow(table_name)
    raw_data = extract(url)
    data = transform(raw_data)
    ingest(data, table_name)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prefect Orchestrator')
    parser.add_argument('--table_name', help='Table for Postgres')
    args = parser.parse_args()

    main_flow(args)
