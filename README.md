# RiskPulse Data Platform — Airflow 3.0 + Databricks + Kubernetes

A production-style end-to-end data platform built from scratch.

## Architecture
## Architecture
REST API (JSONPlaceholder)
↓
Airflow 3.0 (Orchestration - Asset-aware scheduling)
↓
Databricks (Transformation - Medallion Architecture)
↓
Delta Lake (Storage - ACID, Time Travel, Upserts)

## Tech Stack

- **Orchestration:** Apache Airflow 3.0 on Kubernetes (Kind) via Helm
- **Compute:** Databricks (PySpark notebooks)
- **Storage:** Delta Lake (Bronze / Silver / Gold)
- **Data Quality:** Custom DQX-style checks with quarantine routing
- **GitOps:** git-sync sidecar auto-syncs DAGs from GitHub
- **CI/CD:** GitHub Actions + Docker
- **Infrastructure:** Kubernetes (Kind), Helm, PV/PVC for log persistence

## Pipeline Flow
produce_data_assets (Airflow DAG)
→ Fetches posts + users from JSONPlaceholder API
→ Marks Assets as updated
trigger_databricks_workflow_dag (auto-triggered by Assets)
→ bronze_posts: Ingest 100 posts → Delta table
→ bronze_users: Ingest 10 users → Delta table
→ silver_posts: Clean + validate + DQX checks + MERGE upsert
→ gold_most_popular_tags: User engagement metrics
→ gold_posts_users: Joined OBT for analytics

## Key Features

- **Asset-aware scheduling** — downstream DAGs trigger when upstream data is ready, not on a clock
- **Incremental upserts** — Delta MERGE handles late arrivals and deduplication
- **Data quality gating** — bad records routed to quarantine, never silently dropped
- **Time travel** — every table version queryable for audit and compliance
- **GitOps** — push to GitHub, DAGs auto-deploy to cluster in 60 seconds
- **Full audit trail** — Delta history tracks every write with job ID, user, timestamp

## Local Setup

### Prerequisites
- Windows with WSL2 + Docker Desktop
- Kind, kubectl, Helm
- Databricks account (free tier works)

### Install
```bash
git clone https://github.com/kundamnikhil/databricks-airflow3.0-template.git
cd databricks-airflow3.0-template
./install_airflow_with_persistence.sh
```

### Configure
1. Add Databricks connection in Airflow UI (Admin → Connections)
2. Create git-credentials secret (see k8s/secrets/git-secrets.yaml template)
3. Update job IDs in dags/trigger_databricks_workflow_dag.py

## Author
Venkata Nikhil Kundam — [LinkedIn](https://linkedin.com/in/kundamnikhil)
