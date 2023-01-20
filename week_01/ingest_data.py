import pandas as pd
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    source_file = 'output.parquet'
    
    # download parquet 
    os.system(f'wget ' + url + ' -o ' + source_file)

    conexion = 'postgresql://' + user + ':' + password + '@' + host + ':' + port + '/' + db
   
    engine = create_engine(conexion)

    # "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    # homework:
    # "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-01.parquet"
    if url.endswith("parquet"):
        df = pd.read_parquet(url)
    elif url.endswith("csv"):
        df = pd.read_csv(url)

    df.to_sql(name=table_name, con=engine, if_exists="append")

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Script')
    parser.add_argument('--user', help='User for Postgres')
    parser.add_argument('--password', help='Pass for Postgres')
    parser.add_argument('--host', help='Host for Postgres')
    parser.add_argument('--port', help='Port for Postgres')
    parser.add_argument('--db', help='Database for Postgres')
    parser.add_argument('--table_name', help='Table for Postgres')
    parser.add_argument('--url', help='Url for CSV file')

    args = parser.parse_args()

    main(args)