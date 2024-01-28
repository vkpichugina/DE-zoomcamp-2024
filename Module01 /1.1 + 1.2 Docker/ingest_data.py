import argparse
import pandas as pd
import os
from time import time
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table = params.table
    url = params.url

    csv_name = "output.csv"

    os.system(f"wget {url} -O {csv_name}")

    # download the csv
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    df_iter = pd.read_csv(
        csv_name, iterator=True, chunksize=100000
    )  # , compression="gzip")
    df = next(df_iter)

    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table, con=engine, if_exists="replace")

    df.to_sql(name=table, con=engine, if_exists="append")

    i = 0

    while True:
        t_start = time()
        i += 1
        df = next(df_iter)
        # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table, con=engine, if_exists="append")
        t_end = time()
        print(f"inserted chunk %{i}..., took {(t_end-t_start):.3f} second")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", help="Username for Postgres")
    parser.add_argument("--password", help="Password for Postgres")
    parser.add_argument("--host", help="Host for Postgres")
    parser.add_argument("--port", help="Port for Postgres")
    parser.add_argument("--database", help="Database name for Postgres")
    parser.add_argument("--table", help="Table name where we will write results to")
    parser.add_argument("--url", help="URL for the CSV file")

    args = parser.parse_args()
    main(args)
