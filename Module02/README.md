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




