from airflow.sdk import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from produce_data_assets import posts_asset, users_asset

with DAG(
    dag_id="trigger_databricks_workflow_dag",
    schedule=(posts_asset & users_asset)
):
    run_databricks_workflow = DatabricksRunNowOperator(
        task_id="run_databricks_workflow",
        databricks_conn_id="databricks_default",
        job_id="1032766944558702"
    )
    run_databricks_workflow
