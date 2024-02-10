# Analytics Engineering
## Basics

### ETL vs ELT

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module04/img/ETL.png" alt="ETL" width="600"/>

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module04/img/ELT.png" alt="ELT" width="600"/>

### Kimball's Dimensional Modeling

#### Objective
- Deliver data understandable to the business users
- Deliver fast query perfomance

#### Approach
Prioritise user understandability and query perfomance over non redundant data (3NF)


#### Elements of Dimensional Modeling

##### Facts
- Measuremets, metrics or facts
- Corresponds to a business process
- "verbs"

##### Dimensions tables
- Corresponds to a business entity
- Provides context to a business process
- "nouns"

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module04/img/star.png" alt="star" width="400"/>

#### Architecture of Dimensional Modeling

##### Stage Area
- Contains the raw data
- Not meant to be exposed to everyone

##### Processing Area
- From raw data to data models
- Focuses in efficiency and ensuring standards
  
##### Presentation area
- Final presentation of the data
- Exposure to business stakeholder

## DBT (data build tool)
dbt is an open-source command-line tool that allows you to transform data in your data warehouse 
using SQL. 
It's often described as a "data modeling tool" or a "data pipeline tool". 
dbt is a SQL-first transformation workflow that lets teams quickly and collaboratively deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation.

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module04/img/dbt.png" alt="dbt" width="400"/>

### How does it work?
<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module04/img/dbt.png" alt="dbt" width="400"/>

### How to use dbt?
dbt Core: 
open-source project that allows the data transformation
- Builds and runs a dbt project (.sql and .yml files)
- Insludes SQL compilation logic, macros and database adapters
- Includes a CLI interface to run dbt commands
- Open source and free to use

dbt Cloud: 
SaaS app to develop and manage dbt projests
- Web-based IDE and cloud CLI to develop, run and test a dbt project
- Manage Environments
- Jobs orchestration
- Logging and Alering
- Integrated documentation
- Admin and metadata API
- Semantic Layer

<img src="https://github.com/vkpichugina/DE-zoomcamp-2024/blob/main/Module04/img/usage.png" alt="dbt" width="400"/>

