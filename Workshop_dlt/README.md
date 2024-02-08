# DLT workshop 

You can find workshop info by link [data_ingestion_workshop](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/workshops/dlt_resources/data_ingestion_workshop.md).

# Homework

The [linked colab notebook](https://colab.research.google.com/drive/1Te-AT0lfh0GpChg1Rbd0ByEKOHYtWXfm#scrollTo=wLF4iXf-NR7t&forceEdit=true&sandboxMode=true) offers a few exercises to practice what you learned today.


#### Question 1: What is the sum of the outputs of the generator for limit = 5?
- **A**: 10.23433234744176
- **B**: 7.892332347441762
- **C**: 8.382332347441762
- **D**: 9.123332347441762

``` python
def square_root_generator(limit):
    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Example usage:
limit = 5
generator = square_root_generator(limit)

sum=0

for sqrt_value in generator:
    sum+=sqrt_value

print(sum)
```

8.382332347441762

#### Question 2: What is the 13th number yielded by the generator?
- **A**: 4.236551275463989
- **B**: 3.605551275463989
- **C**: 2.345551275463989
- **D**: 5.678551275463989

``` python
def square_root_generator(limit):
    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Example usage:
limit = 13
generator = square_root_generator(limit)

for sqrt_value in generator:
    print(sqrt_value)
```
3.605551275463989

#### Question 3: Append the 2 generators. After correctly appending the data, calculate the sum of all ages of people.
- **A**: 353
- **B**: 365
- **C**: 378
- **D**: 390

Below you have 2 generators. You will be tasked to load them to duckdb and answer some questions from the data
1. Load the first generator and calculate the sum of ages of all people. Make sure to only load it once.
```python
import dlt
import duckdb

def people_1():
    for i in range(1, 6):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

for person in people_1():
    print(person)


def people_2():
    for i in range(3, 9):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}


for person in people_2():
    print(person)

# define the connection to load to.
generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='ages')


# we can load any generator to a table at the pipeline destnation as follows:
info = generators_pipeline.run(people_1(),
										table_name="ages",
										write_disposition="replace")

# the outcome metadata is returned by the load and we can inspect it by printing it.
print(info)

conn = duckdb.connect(f"{generators_pipeline.pipeline_name}.duckdb")

# let's see the tables
conn.sql(f"SET search_path = '{generators_pipeline.dataset_name}'")
print('Loaded tables: ')
display(conn.sql("show tables"))

# and the data

print("\n\n\n ages table below:")

ages = conn.sql("SELECT * FROM ages").df()
display(ages)

sum_ages = conn.sql("SELECT sum(Age) FROM ages").df()
display(sum_ages)
```

Output:

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Workshop_dlt/img/dlt_1.png" alt="DLT" width="600"/>

2. Append the second generator to the same table as the first.
3. After correctly appending the data, calculate the sum of all ages of people.
``` python
import dlt
import duckdb

def people_1():
    for i in range(1, 6):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

for person in people_1():
    print(person)


def people_2():
    for i in range(3, 9):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}


for person in people_2():
    print(person)

# define the connection to load to.
generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='ages')


# we can load any generator to a table at the pipeline destnation as follows:
info = generators_pipeline.run(people_1(),
										table_name="ages",
										write_disposition="replace")

# we can load the next generator to the same or to a different table.
info = generators_pipeline.run(people_2(),
										table_name="ages",
										write_disposition="append")

# the outcome metadata is returned by the load and we can inspect it by printing it.
print(info)

conn = duckdb.connect(f"{generators_pipeline.pipeline_name}.duckdb")

# let's see the tables
conn.sql(f"SET search_path = '{generators_pipeline.dataset_name}'")
print('Loaded tables: ')
display(conn.sql("show tables"))

# and the data

print("\n\n\n ages table below:")

ages = conn.sql("SELECT * FROM ages").df()
display(ages)

sum_ages = conn.sql("SELECT sum(Age) FROM ages").df()
display(sum_ages)
```
Output:

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Workshop_dlt/img/dlt_2.png" alt="DLT" width="600"/>

#### Question 4: Merge the 2 generators using the ID column. Calculate the sum of ages of all the people loaded as described above.
- **A**: 205
- **B**: 213
- **C**: 221
- **D**: 230

```python
# to do: homework :)
import dlt
import duckdb

def people_1():
    for i in range(1, 6):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}

for person in people_1():
    print(person)


def people_2():
    for i in range(3, 9):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}


for person in people_2():
    print(person)

# define the connection to load to.
generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='ages')


# we can load any generator to a table at the pipeline destnation as follows:
info = generators_pipeline.run(people_1(),
										table_name="ages",
										write_disposition="replace")

# we can load the next generator to the same or to a different table.
info = generators_pipeline.run(people_2(),
										table_name="ages",
                    primary_key= "id",
 									write_disposition="merge")


conn = duckdb.connect(f"{generators_pipeline.pipeline_name}.duckdb")

# let's see the tables
conn.sql(f"SET search_path = '{generators_pipeline.dataset_name}'")
print('Loaded tables: ')
display(conn.sql("show tables"))

# and the data

print("\n\n\n ages table below:")

ages = conn.sql("SELECT * FROM ages").df()
display(ages)

sum_ages = conn.sql("SELECT sum(Age) FROM ages").df()
display(sum_ages)
```
<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Workshop_dlt/img/dlt_3.png" alt="DLT" width="600"/>

