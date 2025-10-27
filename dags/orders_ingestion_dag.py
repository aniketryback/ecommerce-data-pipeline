from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ingestion_orders import ingest_orders

default_args = {
    'owner': 'aniket',
    'depends_on_past': False,
    'email': ['aniket@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='orders_ingestion_dag',
    default_args = default_args,
    description = 'Dag to ingest daily interval data',
    schedule = '@daily',
    start_date = datetime(2025,10,24),
    catchup = False,
    tags=['ingestion', 'ecommerce']

)as dag:
    
        ingest_task = PythonOperator(
            task_id = 'ingest_orders',
            python_callable = ingest_orders
        )

        ingest_task