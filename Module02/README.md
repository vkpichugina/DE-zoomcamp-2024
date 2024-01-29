<img width="916" alt="Снимок экрана 2024-01-29 в 14 29 25" src="https://github.com/vkpichugina/DE-zoomcamp-2024/assets/132204881/3ec88d8c-6613-4e9d-9ca5-85b8217d8c67"># Workflow Orchestration
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





