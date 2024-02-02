# Docker
Docker is a containerization software that allows us to isolate software in a similar way to virtual machines but in a much leaner way.

A Docker image is a snapshot of a container that we can define to run our software, or in this case our data pipelines. By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can run our containers there.

Docker provides the following advantages:

- Reproducibility
- Local experimentation
- Integration tests (CI/CD)
- Running pipelines on the cloud (AWS Batch, Kubernetes jobs)
- Spark (analytics engine for large-scale data processing)
- Serverless (AWS Lambda, Google functions)
  
Docker containers are stateless: any changes done inside a container will NOT be saved when the container is killed and started again. This is an advantage because it allows us to restore any container to its initial state in a reproducible manner, but you will have to store data elsewhere if you need to do so; a common way to do so is with volumes.
## Setting up Docker Environment 

1. **Install Docker**: Install Docker from the official Docker website, tailored to your specific operating system.
2. **Confirm Installation**: Validate the Docker installation by executing the “docker version” command in a terminal or command prompt.
3. **Obtain Docker Images**: Retrieve essential Docker images from Docker Hub using the “docker pull” command and the corresponding image name.
4. **Formulate a Dockerfile**: Craft a text file called “Dockerfile”, encompassing the necessary directives for constructing the desired container image.
5. **Construct the Docker Image**: Execute the “docker build” command, specifying the directory housing the Dockerfile to fabricate the image.
6. **Launch Containers**: Commence container instances based on the built images using the “docker run” command with suitable options.
7. **Manage Containers**: Effectively handle containers using various Docker commands such as “docker ps” to enlist running containers and “docker stop” to halt their execution.

## Docker commands
- **sudo service docker start** - to start docker
- **docker run** - initiates creating and activating a fresh container using a Docker image
- **docker ps** - presents data regarding the active containers on a Docker host
- **docker images** - displays a collection of Docker images stored locally
- **docker stop all containers** - halts all active containers simultaneously
- **docker rm** - deletes one or more stopped containers from the system
- **docker rmi** - erases one or more Docker images from the local environment
- **docker build** - constructs a new Docker image based on instructions provided in a Dockerfile (use -t to create a name)
  - ```build -t my_container```
- **docker push** - uploads a Docker image to a registry, like Docker Hub or a private registry. This facilitates sharing the image with others or deploying it in different environments
- **docker pull** - retrieves a Docker image from a registry to the local system
- **docker-compose (up/down)** - used for defining and controlling multi-container applications. It employs a YAML file to specify the necessary services, networks, and volumes for the application, simplifying the deployment process
- **docker network** -  manages networks that enable communication between containers
- **docker volume** - handles persistent data storage for containers.
- **docker logs** - retrieves container-generated logs, displaying output and error messages

## How to work with docker

1) Create a dockerfile
2) Run the command `docker build -t <image_name>:<tag>`
3) Run the container `docker run -it <image_name>:<tag> <argument>`

### Example with running postgres in a container

Create a folder anywhere you'd like for Postgres to store data in. We will use the example folder `ny_taxi_postgres_data`. Here's how to run the container:

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```
- The container needs 3 environment variables:
    - `POSTGRES_USER` is the username for logging into the database. We chose `root`.
    - `POSTGRES_PASSWORD` is the password for the database. We chose `root`
    - `POSTGRES_DB` is the name that we will give the database. We chose `ny_taxi`.
- `-v` points to the volume directory. The colon `:` separates the first part (path to the folder in the host computer) from the second part (path to the folder inside the container).
    - Path names must be absolute. If you're in a UNIX-like system, you can use `pwd` to print you local folder as a shortcut; this example should work with both `bash` and `zsh` shells, but `fish` will require you to remove the `$`.
    - This command will only work if you run it from a directory which contains the `ny_taxi_postgres_data` subdirectory you created above.
- The `-p` is for port mapping. We map the default Postgres port to the same port in the host.
- The last argument is the image name and tag. We run the official `postgres` image on its version `13`.

Once the container is running, we can log into our database with [pgcli](https://www.pgcli.com/) with the following command:

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
- `-h` is the host. Since we're running locally we can use `localhost`.
- `-p` is the port.
- `-u` is the username.
- `-d` is the database name.
- The password is not provided; it will be requested after running the command.

### Connecting pgAdmin and Postgres with Docker networking

Let's create a virtual Docker network called `pg-network`:

```bash
docker network create pg-network
```

>You can remove the network later with the command `docker network rm pg-network` . You can look at the existing networks with `docker network ls` .

We will now re-run our Postgres container with the added network name and the container network name, so that the pgAdmin container can find it (we'll use `pg-database` for the container name):

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
```

We will now run the pgAdmin container on another terminal:

```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```
* The container needs 2 environment variables: a login email and a password. We use `admin@admin.com` and `root` in this example.
* pgAdmin is a web app and its default port is 80; we map it to 8080 in our localhost to avoid any possible conflicts.
* Just like with the Postgres container, we specify a network and a name. However, the name in this example isn't really necessary because there won't be any containers trying to access this particular container.
* The actual image name is `dpage/pgadmin4` .

You should now be able to load pgAdmin on a web browser by browsing to `localhost:8080`. Use the same email and password you used for running the container to log in.


### Using the ingestion script with Docker

The ingestion script:
```python
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
```

We can test the script with the following command:
```bash
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```

### Dockerizing the script

Create a following dockerfile that includes `ingest_data.py` script and create a new image:
```dockerfile
FROM python:3.9.1

# We need to install wget to download the csv file
RUN apt-get install wget
# psycopg2 is a postgres db adapter for python: sqlalchemy needs it
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]
```
Build the image:
```bash
docker build -t taxi_ingest:v001 .
```

And run it:
```bash
docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```
* We need to provide the network for Docker to find the Postgres container. It goes before the name of the image.
* Since Postgres is running on a separate container, the host argument will have to point to the container name of Postgres.
* You can drop the table in pgAdmin beforehand if you want, but the script will automatically replace the pre-existing table.

### Running Postgres and pgAdmin with Docker-compose

`docker-compose` allows us to launch multiple containers using a single configuration file, so that we don't have to run multiple complex `docker run` commands separately.

Docker compose makes use of YAML files. Here's the `docker-compose.yaml` file for running the Postgres and pgAdmin containers:

```yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    volumes:
      - "./data_pgadmin:/var/lib/pgadmin"
    ports:
      - "8080:80"
```

We can now run Docker compose by running the following command from the same directory where `docker-compose.yaml` is found. Make sure that all previous containers aren't running anymore:

```bash
docker-compose up
```

You will have to press Ctrl+C in order to shut down the containers. The proper way of shutting them down is with this command:

```bash
docker-compose down
```

And if you want to run the containers again in the background rather than in the foreground (thus freeing up your terminal), you can run them in detached mode:

```bash
docker-compose up -d
```
