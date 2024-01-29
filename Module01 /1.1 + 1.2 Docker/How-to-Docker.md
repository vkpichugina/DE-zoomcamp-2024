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

## Creating a custom pipeline with Docker

_([Video source](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=3))_

Let's create an example pipeline. We will create a dummy `pipeline.py` Python script that receives an argument and prints it.

```python
import sys
import pandas # we don't need this but it's useful for the example

# print arguments
print(sys.argv)

# argument 0 is the name os the file
# argumment 1 contains the actual first argument we care about
day = sys.argv[1]

# cool pandas stuff goes here

# print a sentence with the argument
print(f'job finished successfully for day = {day}')
```

We can run this script with `python pipeline.py <some_number>` and it should print 2 lines:
* `['pipeline.py', '<some_number>']`
* `job finished successfully for day = <some_number>`

Let's containerize it by creating a Docker image. Create the folllowing `Dockerfile` file:

```dockerfile
# base Docker image that we will build on
FROM python:3.9.1

# set up our image by installing prerequisites; pandas in this case
RUN pip install pandas

# set up the working directory inside the container
WORKDIR /app
# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["python", "pipeline.py"]
```

Let's build the image:


```ssh
docker build -t test:pandas .
```
* The image name will be `test` and its tag will be `pandas`. If the tag isn't specified it will default to `latest`.

We can now run the container and pass an argument to it, so that our pipeline will receive it:

```ssh
docker run -it test:pandas some_number
```

You should get the same output you did when you ran the pipeline script by itself.

>Note: these instructions asume that `pipeline.py` and `Dockerfile` are in the same directory. The Docker commands should also be run from the same directory as these files.
