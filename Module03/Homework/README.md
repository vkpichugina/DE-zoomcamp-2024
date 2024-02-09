# Homework

> You will need to use the PARQUET option files when creating an External Table

SETUP:
Create an external table using the Green Taxi Trip Records Data for 2022.

```sql
create or replace external table de-zoomcamp-bq.ny_taxi.green_taxi_data_22
options (
  format = 'PARQUET',
  uris=['gs://green-taxi-data-2022/green_tripdata_2022-*.parquet','gs://green-taxi-data-2022/green_tripdata_2023-*.parquet']
);
```
Create a table in BQ using the Green Taxi Trip Records for 2022 (do not partition or cluster this table).

```
create or replace table de-zoomcamp-bq.ny_taxi.green_taxi_data_22_non_partitoned as
select * from de-zoomcamp-bq.ny_taxi.green_taxi_data_22;
```

### Question 1: 
What is count of records for the 2022 Green Taxi Data?

```sql
select count(*) from de-zoomcamp-bq.ny_taxi.green_taxi_data_22
```
or check table Details --> Number of rows: 840402

### Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```sql
select distinct PULocationID from de-zoomcamp-bq.ny_taxi.green_taxi_data_22; --0 MB

select distinct PULocationID from de-zoomcamp-bq.ny_taxi.green_taxi_data_22_non_partitoned; --6.41 MB
```

0 MB for the External Table and 6.41MB for the Materialized Table

### Question 3:

How many records have a fare_amount of 0?

```sql
select count(*) from de-zoomcamp-bq.ny_taxi.green_taxi_data_22_non_partitoned
where fare_amount=0; --1622
```

### Question 4

What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

```sql
create or replace table de-zoomcamp-bq.ny_taxi.green_taxi_data_22_for_q
partition by date(lpep_pickup_datetime)
cluster by PUlocationID as
select * from de-zoomcamp-bq.ny_taxi.green_taxi_data_22;
```

Partition by lpep_pickup_datetime Cluster on PUlocationID

### Question 5
Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

```sql
select distinct PULocationID
from  de-zoomcamp-bq.ny_taxi.green_taxi_data_22_non_partitoned
where lpep_pickup_datetime between '2022-06-01' AND '2022-06-30'; --12,82 MB

select distinct PULocationID
from  de-zoomcamp-bq.ny_taxi.green_taxi_data_22_for_q
where lpep_pickup_datetime between '2022-06-01' AND '2022-06-30'; --1,12 MB 
```

12.82 MB for non-partitioned table and 1.12 MB for the partitioned table

### Question 6
Where is the data stored in the External Table you created?

Big Query
**GCP Bucket**
Big Table
Container Registry

### Question 7
It is best practice in Big Query to always cluster your data:

True
**False**


### (Bonus: Not worth points) Question 8:

No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? 
0 B

Why?
It tales info from metadata
