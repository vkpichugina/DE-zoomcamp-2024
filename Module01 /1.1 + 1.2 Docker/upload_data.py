import pandas as pd
from time import time
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

df_iter = pd.read_csv('/Users/vkpichugina/downloads/yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)

df = next(df_iter)

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

i=0

while True:
    t_start=time()
    i+=1
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
    t_end = time()
    print(f'inserted chunk %{i}..., took {(t_end-t_start):.3f} second' )



