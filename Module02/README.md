# Workflow Orchestration
## What will we build
<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module02/Flow.png" alt="Architecture" width="600"/>

### Architecture
#### Extract
Pull data from a source (API - NYC taxi dataset)
#### Transform
Data cleaning, transformation and partitioning
#### Load
API to Mage, Mage to Postgres, GCS, BigQuery

### Orchestration
Orchestration is a process of dependency management, facilitated through **automation**.

The data orchestrator manages scheduling, triggering, monitoring and even resource allocation.

- Every workflow requires sequential steps
  - steps = tasks
  - workflows = DAGs (directed acyclic graphs)

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module02/DE-lifecycle.png" alt="DE-lifestyle" width="600"/>

### What does a good solution look like?
A good orchestrator handles...
- Workflow management
- Automation
- Error handling
- Recovery
- Monitoring, alerting
- Resoruce optimizatoin
- Observability
- Debugging
- Compliance/Auditing

A good orchestrator prioritizes...

The developer experience
- Flow state
- Feedback Loops
- Cognitive Load

## What is Mage?

An open-source pipeline tool for orchestraiting, transforming and integrating data

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module02/Mage-1.png" alt="Mage flow" width="600"/>

### Anatomy of a Block

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module02/Mage-block.png" alt="Anatomy of a Block" width="600"/>

Function returnes DataFrame

## Configuring Mage

See the instruction in [mage-zoomcamp](https://github.com/mage-ai/mage-zoomcamp)

To update mage run:

```bash
docker pull mageai/mageai:latest
```

## Configuring Postgres

How to configure a Postgres client to connect to a local Postgres database  in a Docker image build.

```Dockerfile
version: '3'
services:
  magic:
    image: mageai/mageai:latest
    command: mage start ${PROJECT_NAME}
    env_file:
      - .env
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      USER_CODE_PATH: /home/src/${PROJECT_NAME}
      POSTGRES_DBNAME: ${POSTGRES_DBNAME}
      POSTGRES_SCHEMA: ${POSTGRES_SCHEMA}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_HOST: ${POSTGRES_HOST}
      POSTGRES_PORT: ${POSTGRES_PORT}
    ports:
      - 6789:6789
    volumes:
      - .:/home/src/
      - ~/Documents/secrets/personal-gcp.json:/home/src/personal-gcp.json
    restart: on-failure:5
  postgres:
    image: postgres:14
    restart: on-failure
    container_name: ${PROJECT_NAME}-postgres
    env_file:
      - .env
    environment:
      POSTGRES_DB: ${POSTGRES_DBNAME}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
```

in .env file we have information about the connection like:

```environment
PROJECT_NAME=magic-zoomcamp
POSTGRES_DBNAME=postgres
POSTGRES_SCHEMA=magic
POSTGRES_USER=postgres
POSTGRES_PASSWORD=*****
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

> Benefit: .env almost always in gitignore files - so we don't occasionally commit these files to version control

Adding Dev connection profile in Mage io_config.yaml - useful for separation development and production:

```yaml
dev:
    # PostgresSQL
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{ env_var('POSTGRES_DBNAME') }}"
  POSTGRES_SCHEMA: "{{ env_var('POSTGRES_SCHEMA') }}" 
  POSTGRES_USER: "{{ env_var('POSTGRES_USER') }}"
  POSTGRES_PASSWORD: "{{ env_var('POSTGRES_PASSWORD') }}"
  POSTGRES_HOST: "{{ env_var('POSTGRES_HOST') }}"
  POSTGRES_PORT: "{{ env_var('POSTGRES_PORT') }}"
```
To check the connection to docker's postgres:  create a new pipeline "test_config" and add SQL data loader, select connection to PostgreSQL and profile dev. Run command:
```sql
select 1;
```
<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module02/img/connection_check.png" alt="Architecture" width="600"/>

## ETL: API to Postgres

1) Create a new pipeline "API_to_postgres"
2) Create a new data laoder Python --> API "load_api_data"
3) Edit the template
   - add correct url to the file
   - exclude response
   - map datatypes (reduce memory usage, the pipeline fail if datatypes change on the source)
   - do native date parsing
   - return csv file using pandas.read_csv
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
    """
    Template for loading data from API
    """
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                }
    # native date parsing 
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    return pd.read_csv(
        url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
        )


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

     ```
4) Add transformer: Transformer --> Python --> Generic (no template) "transform_taxi_data"
5) We want to exclude data where passenger_count=0:
   ```python
   print( f'Preprocessing: rows with zero passengers { data["passenger_count"].isin([0]).sum()}')
    return data[data['passenger_count']>0]
   ```
6) Add test that there are no rows with zero passengers in output:
   ```python
   @test
    def test_output(output, *args):
    assert output["passenger_count"].isin([0]).sum()==0, 'There are rides with zero passengers'
   ```
7) Add Data Exporter: Data Exporter --> Python --> Postgres "taxi_data_to_postgres"
8) Specify schema, table and profile:
   ```python
    schema_name = 'ny_taxi'  # Specify the name of the schema to export data to
    table_name = 'yellow_taxi_data'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'
   ```
9) To check that work add Data Loader --> SQL "load_taxi_data". Select connection to PostgreSQL profile dev, Use row SQL. Run command:
   ```sql
    select * from ny_taxi.yellow_taxi_data limit 10
   ```

   <img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module02/img/ETL-1.png" alt="Architecture" width="600"/>

## Configuring GCP

1) Create a new bucket: Search --> Google Cloud Storage --> Cloud Storage "mage-zoomcamp-vkpichugina"
2) Create a service account "mage-zoomcamp" with role "owner"
3) Create a new json key and add it to mage-zoomcamp folder
4) Authentification: Mages --> Files --> io_config.yaml Add path to json file in google section
 ```yaml
   # Google
  GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/path/to/your/service/account/key.json"
  GOOGLE_LOCATION: US # Optional
   ```
5) Pipelines --> test_config --> switch connection to BigQuery and switch profile to default




