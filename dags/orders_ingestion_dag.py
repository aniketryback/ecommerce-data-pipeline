from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'aniket',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    
}

with DAG(
    dag_id='orders_ingestion_dag',
    default_args=default_args,
    description='Daily ingestion of multiple order CSVs and upload to S3',
    schedule='0 6 * * *',
    start_date=datetime(2025, 10, 27),
    catchup=False
) as dag:

    run_ingestion = BashOperator(
    task_id='run_ingestion_script',
    bash_command='python /usr/local/airflow/dags/scripts/ingestion_orders.py',
    dag=dag
)
