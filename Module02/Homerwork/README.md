# Homework Module 2

The goal will be to construct an ETL pipeline that loads the data, performs some transformations, and writes the data to a database (and Google Cloud!).

- Create a new pipeline, call it `green_taxi_etl`
### Data Loader Block
- Add a data loader block and use Pandas to read data for the final quarter of 2020 (months `10`, `11`, `12`).
  - You can use the same datatypes and date parsing methods shown in the course.
  - `BONUS`: load the final three months using a for loop and `pd.concat`
```python
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    df=pd.DataFrame()
    for i in range(10, 13):
        url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{i}.csv.gz'
        taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'RatecodeID':pd.Int64Dtype(),
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,	
                    'ehail_fee':float,
                    'improvement_surcharge':float,
                    'total_amount':float,	
                    'payment_type': pd.Int64Dtype(),
                    'trip_type': pd.Int64Dtype(),
                    'congestion_surcharge':float
                }
        # native date parsing 
        parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
        df= pd.concat([df, pd.read_csv(
            url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
    )]
              )
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
```
#### Question 1. Data Loading

Once the dataset is loaded, what's the shape of the data?

* **266,855 rows x 20 columns**
* 544,898 rows x 18 columns
* 544,898 rows x 20 columns
* 133,744 rows x 20 columns

### Transformer Block
- Add a transformer block and perform the following:
  - Remove rows where the passenger count is equal to 0 _or_ the trip distance is equal to zero.
  - Create a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date.
  - Rename columns in Camel Case to Snake Case, e.g. `VendorID` to `vendor_id`.
  - Add three assertions:
    - `vendor_id` is one of the existing values in the column (currently)
    - `passenger_count` is greater than 0
    - `trip_distance` is greater than 0
      
```python
import re
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
# Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
# Rename columns in Camel Case to Snake Case
@transformer
def transform(data, *args, **kwargs):

    # Specify your transformation logic here
    print( f'Preprocessing: rows with zero passengers { data["passenger_count"].isin([0]).sum()}')
    print( f'Preprocessing: rows with zero distance { data["trip_distance"].isin([0]).sum()}')
    data['lpep_pickup_date']=data['lpep_pickup_datetime'].dt.date
    data.columns = (data.columns
                 .str.replace('ID','_id')
                .str.lower()
        )
    return data[(data['passenger_count']>0) & (data['trip_distance']>0) ]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def test_output(output, *args):
    # `passenger_count` is greater than 0
    assert output["passenger_count"].isin([0]).sum()==0, 'There are rides with zero passengers'
    # `trip_distance` is greater than 0
    assert output["trip_distance"].isin([0]).sum()==0, 'There are rides with zero distance'
    #vendor_id is one of the existing values in the column (currently)
    assert output["vendor_id"].isin([1,2]).all() == True, 'There are vendors that are not in the list'
```

#### Question 2. Data Transformation

Upon filtering the dataset where the passenger count is greater than 0 _and_ the trip distance is greater than zero, how many rows are left?

* 544,897 rows
* 266,855 rows
* **139,370 rows**
* 266,856 rows

#### Question 3. Data Transformation

Which of the following creates a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date?

* `data = data['lpep_pickup_datetime'].date`
* `data('lpep_pickup_date') = data['lpep_pickup_datetime'].date`
* **`data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`**
* `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt().date()`

#### Question 4. Data Transformation

What are the existing values of `VendorID` in the dataset?

* 1, 2, or 3
* **1 or 2**
* 1, 2, 3, 4
* 1

#### Question 5. Data Transformation

How many columns need to be renamed to snake case?

* 3
* 6
* 2
* **4** (VendorID RatecodeID PULocationID DOLocationID)

### Data Exporter Block
- Using a Postgres data exporter (SQL or Python), write the dataset to a table called `green_taxi` in a schema `mage`. Replace the table if it already exists.
  ```sql
  ```
- Write your data as Parquet files to a bucket in GCP, partioned by `lpep_pickup_date`. Use the `pyarrow` library!
  ```python
  ```
- Schedule your pipeline to run daily at 5AM UTC.