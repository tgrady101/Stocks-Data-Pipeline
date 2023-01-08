import os
import logging
import Load_Current_SP_500_End_of_Day_Prices_Into_GCS
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import storage
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitPySparkJobOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get('GCP_BQ_DATASET')
CLUSTER_NAME = "move-stock-data"
CLUSTER_REGION = "us-central1"
PYSPARK_FILE = "Move_Current_SP_500_Data_From_GCS_to_BigQuery.py"
DBT_DIR = os.path.join(AIRFLOW_HOME, "dbt")

CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},
    },
}

default_args = {
    "owner": "airflow",
    "start_date": "2023-01-04 00:00",
    "depends_on_past": False,
    "retries": 0,
    "dbt_cloud_conn_id": "dbt_cloud",
    "account_id": 136764

}

with DAG(
    dag_id="stock_data_pipeline_dag",
    schedule_interval="15 23 * * 1-5",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['stock-pipline'],
) as dag:

    upload_SP_500_data_to_datalake_task = PythonOperator(
    task_id="upload_SP_500_data_to_datalake_task",
    python_callable=Load_Current_SP_500_End_of_Day_Prices_Into_GCS.main,
    dag=dag
    )
    create_cluster_dataproc_task = DataprocCreateClusterOperator(
        task_id="create_cluster_dataproc_task",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=CLUSTER_REGION,
        trigger_rule="all_success",
        cluster_name=CLUSTER_NAME
    )

    submit_spark_job_task = DataprocSubmitPySparkJobOperator(
        task_id = "submit_dataproc_spark_job_task",
        main = f"gs://{BUCKET}/{PYSPARK_FILE}",
        cluster_name = CLUSTER_NAME,
        region = CLUSTER_REGION,
        dataproc_jars = ["gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.27.1.jar"]
    )

    delete_cluster_dataproc_task = DataprocDeleteClusterOperator(
        task_id="delete_cluster_dataproc_task",
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        region=CLUSTER_REGION,
        trigger_rule="all_done"
    )

    trigger_dbt_cloud_job_run = DbtCloudRunJobOperator(
        task_id="trigger_dbt_cloud_job_run",
        job_id=192464,
        check_interval=10,
        timeout=300,
    )

    upload_SP_500_data_to_datalake_task >> create_cluster_dataproc_task >> submit_spark_job_task >> delete_cluster_dataproc_task >> trigger_dbt_cloud_job_run