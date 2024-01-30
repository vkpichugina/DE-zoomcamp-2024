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

## Configure Mage

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




