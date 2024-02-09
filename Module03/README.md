# Data Warehouse

This lesson will cover the topics of _Data Warehouse_ and _BigQuery_.
# OLAP vs OLTP
In Data Science, when we're discussing data processing systems, there are 2 main types: **OLAP** and **OLTP** systems.

* ***OLTP***: Online Transaction Processing.
* ***OLAP***: Online Analytical Processing.

An intuitive way of looking at both of these systems is that OLTP systems are "classic databases" whereas OLAP systems are catered for advanced data analytics purposes.

|   | OLTP | OLAP |
|---|---|---|
| Purpose | Control and run essential business operations in real time | Plan, solve problems, support decisions, discover hidden insights |
| Data updates | Short, fast updates initiated by user | Data periodically refreshed with scheduled, long-running batch jobs |
| Database design | Normalized databases for efficiency | Denormalized databases for analysis |
| Space requirements | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| Backup and recovery | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| Productivity | Increases productivity of end users | Increases productivity of business managers, data analysts and executives |
| Data view | Lists day-to-day business transactions | Multi-dimensional view of enterprise data |
| User examples | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts and executives |


# Data Warehouse

A **Data Warehouse** (DWH) is an ***OLAP solution*** meant for ***reporting and data analysis***. Unlike Data Lakes, which follow the ELT model, DWs commonly use the ETL model.

A DW receives data from different ***data sources*** which is then processed in a ***staging area*** before being ingested to the actual warehouse (a database) and arranged as needed. DWs may then feed data to separate ***Data Marts***; smaller database systems which end users may use for different purposes.

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module03/img/DWH_1.png" alt="DWH" width="600"/>

# BigQuery

BigQuery (BQ) is a Data Warehouse solution offered by Google Cloud Platform.

- Serverless data warehouse.
  - There are no servers to manage or database software to install; this is managed by Google and it's transparent to the customers.
- Software as well as infrastructure including
  - **scalability** and  **high-availability**. Google takes care of the underlying software and infrastructure.
- Built-in features like
  - Machine Learning
  - Geospatial Analysis 
  - Business Intelligence 
- BQ maximizes flexibility by separating data analysis and storage in different _compute engines_, thus allowing the customers to budget accordingly and reduce costs.

Some alternatives to BigQuery from other cloud providers would be AWS Redshift or Azure Synapse Analytics.

## Pricing

BigQuery pricing is divided in 2 main components: processing and storage. There are also additional charges for other operations such as ingestion or extraction. The cost of storage is fixed and at the time of writing is US$0.02 per GB per month; you may check the current storage pricing [in this link](https://cloud.google.com/bigquery/pricing#storage).

Data processing has a [2-tier pricing model](https://cloud.google.com/bigquery/pricing#analysis_pricing_models):
*  On demand pricing (default): US$5 per TB per month; the first TB of the month is free.
*  Flat rate pricing: based on the number of pre-requested _slots_ (virtual CPUs).
   *  A minimum of 100 slots is required for the flat-rate pricing which costs US$2,000 per month.
   *  Queries take up slots. If you're running multiple queries and run out of slots, the additional queries must wait until other queries finish in order to free up the slot. On demand pricing does not have this issue.
   *  The flat-rate pricing only makes sense when processing more than 400TB of data per month.
  
When running queries on BQ, the top-right corner of the window will display an approximation of the size of the data that will be processed by the query. Once the query has run, the actual amount of processed data will appear in the _Query results_ panel in the lower half of the window. This can be useful to quickly calculate the cost of the query.

# Clustering and patitions
## Partitions

BQ tables can be ***partitioned*** into multiple smaller tables. For example, if we often filter queries based on date, we could partition a table based on date so that we only query a specific sub-table based on the date we're interested in.

[Partition tables](https://cloud.google.com/bigquery/docs/partitioned-tables) are very useful to improve performance and reduce costs, because BQ will not process as much data per query.

You may partition a table by:
* ***Time-unit column***: tables are partitioned based on a `TIMESTAMP`, `DATE`, or `DATETIME` column in the table.
* ***Ingestion time***: tables are partitioned based on the timestamp when BigQuery ingests the data.
* ***Integer range***: tables are partitioned based on an integer column.

For Time-unit and Ingestion time columns, the partition may be daily (the default option), hourly, monthly or yearly.

>Note: BigQuery limits the amount of partitions to 4000 per table. If you need more partitions, consider [clustering](#clustering) as well.


<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module03/img/BQ_partition.png" alt="BQ partition" width="600"/>

```sql

create schema ny_taxi;

create or replace external table de-zoomcamp-bq.ny_taxi.green_taxi_data_22
options (
  format = 'PARQUET',
  uris=['gs://green-taxi-data-2022/green_tripdata_2022-*.parquet','gs://green-taxi-data-2022/green_tripdata_2023-*.parquet']
);

-- Check green trip data
select * from de-zoomcamp-bq.ny_taxi.green_taxi_data_22 limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE de-zoomcamp-bq.ny_taxi.green_taxi_data_22_non_partitoned AS
SELECT * FROM de-zoomcamp-bq.ny_taxi.green_taxi_data_22;


-- Create a partitioned table from external table
CREATE OR REPLACE TABLE de-zoomcamp-bq.ny_taxi.green_taxi_data_22_partitoned
PARTITION BY
  DATE(lpep_pickup_datetime) AS
SELECT * FROM de-zoomcamp-bq.ny_taxi.green_taxi_data_22;

-- Impact of partition
-- Scanning 12.82 MB of data
SELECT DISTINCT(VendorID)
FROM de-zoomcamp-bq.ny_taxi.green_taxi_data_22_non_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Scanning 1.12 MB of DATA
SELECT DISTINCT(VendorID)
FROM de-zoomcamp-bq.ny_taxi.green_taxi_data_22_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `ny_taxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'green_taxi_data_22_partitoned'
ORDER BY total_rows DESC;
```

## Clustering

***Clustering*** consists of rearranging a table based on the values of its columns so that the table is ordered according to any criteria. Clustering can be done based on one or multiple columns up to 4; the ***order*** of the columns in which the clustering is specified is important in order to determine the column priority.

Clustering may improve performance and lower costs on big datasets for certain types of queries, such as queries that use filter clauses and queries that aggregate data.

>Note: tables with less than 1GB don't show significant improvement with partitioning and clustering; doing so in a small table could even lead to increased cost due to the additional metadata reads and maintenance needed for these features.

Clustering columns must be ***top-level***, ***non-repeated*** columns. The following datatypes are supported:
* `DATE`
* `BOOL`
* `GEOGRAPHY`
* `INT64`
* `NUMERIC`
* `BIGNUMERIC`
* `STRING`
* `TIMESTAMP`
* `DATETIME`

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module03/img/BQ_clustering.png" alt="BQ clustering" width="600"/>


```sql
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE de-zoomcamp-bq.ny_taxi.green_taxi_data_22_partitioned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM de-zoomcamp-bq.ny_taxi.green_taxi_data_22;

-- Query scans 7.28 MB
SELECT count(*) as trips
FROM de-zoomcamp-bq.ny_taxi.green_taxi_data_22_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-12-31'
  AND VendorID=1;

-- Query scans 7.07 MB
SELECT count(*) as trips
FROM de-zoomcamp-bq.ny_taxi.green_taxi_data_22_partitioned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-12-31'
  AND VendorID=1;
```

## BigQuery partition
- Time-unit column
- Ingestion time (_PARTITIONTIME)
- Integer range partitionung
- When using Time unit or ingestion time
   - daily
   - hourly
   - monthly or yearly
- Number of patition limit is 4000

## BigQuery Clustering
- Columns you specify are used to colocate related data
- Order of the colimn is important
- The order of the specified columns determines the sort order of the data
- Clustering improves
    - filter queries
    - aggregate queries
- Table with data size < 1 GB don't show significant impovement with partitioning and clustering
- You can specify up to four clustering columns

## Partitioning vs Clustering

| Clustering | Partitioning |
|---|---|
| Cost benefit unknown. BQ cannot estimate the reduction in cost before running a query. | Cost known upfront. BQ can estimate the amount of data to be processed before running a query. |
| High granularity. Multiple criteria can be used to sort the table. | Low granularity. Only a single column can be used to partition the table. |
| Clusters are "fixed in place". | Partitions can be added, deleted, modified or even moved between storage options. |
| Benefits from queries that commonly use filters or aggregation against multiple particular columns. | Benefits when you filter or aggregate on a single column. |
| Unlimited amount of clusters; useful when the cardinality of the number of values in a column or group of columns is large. | Limited to 4000 partitions; cannot be used in columns with larger cardinality. |

## Clustering over partitioning 
- partitioning results in a small amount of data per partition (too much granularity in partition column)
- partitioning would result in over 4000 partitions 
- partitioning results in your mutation operations modify the majority of partitions in the table frequently (for example, writing to the table every few minutes and writing to most of the partitions each time rather than just a handful).

## Automatic reclustering
When new data is written to a table
- it can be written to blocks that contain key ranges that overlap with the key ranges in previously written blocks
- these overlapping keys weaken the sort property of the table
  
To maintain the perfomance characteristics of a clustered table
- BQ will perform automatic reclustering in the background to restore the sort properties of the table.
- For partitioned tables, clustering is maintaned for data within the scope of each partition.


# Best practices

- Cost reduction
  - Avoid SELECT *
  - Price your queries before running them
  - Use clustered or partitioned tables
  - Use streaming inserts with caution as these can increase costs drastically
  - Display query results in stages
  - Use external data sources appropriately as storage in GCS also incurs costs.


- Query perfomance
  - **Partitioning and Clustering:** Partitioning tables and clustering data in BigQuery can significantly improve query performance by limiting the amount of data scanned.
  - **Avoid Oversharding Tables:** Avoid creating too many table partitions (shards), as this can lead   to suboptimal query performance.
  - **Denormalize Data:** Consider using nested or repeated columns instead of excessive normalization to reduce the need for joins and improve performance.
  - **Filter Data Before Joining:** Apply filters to your data before performing joins to reduce the amount of data being joined.
  - **Do Not Treat the WITH Clause as Prepared Statements:** A prepared statement is run and optimized once. It is not reevaluated by the query optimizer each time the query is run.  
  - **Avoid JavaScript User-Defined Functions:** They may not perform as efficiently as native BigQuery functions. 
  - **Use Approximate Aggregate Functions (HyperLog++):** When exact precision is not required, consider using approximate aggregate functions for faster results.
  - **Order By Last:** If possible, use ORDER BY as the last operation in your query for better performance.
  - **Optimize Join Patterns:** Optimize your query's join patterns to minimize data movement and improve query efficiency.
  - **Arrange Tables by Size:** When performing joins, place the table with the largest number of rows first, followed by the table with fewer rows, and so on, in decreasing order of size.
 
# Internals of BQ

A high-level architecture for BQ service:

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module03/img/BQ_arch.png" alt="BQ architecture" width="600"/>

Columnar and record oriented storage:

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module03/img/col_vs_rec.png" alt="Columnar and record oriented storage" width="600"/>

These provide better aggregation and we usually query only few columns, and filter on another columns.

Example of Dremel serving tree:

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module03/img/dremel_tree.png" alt="Dremel serving tree" width="600"/>

