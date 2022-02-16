from datetime import timedelta

import requests
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


default_args = {
    "start_date": days_ago(0),
    "depends_on_past": False,
}

airflow_dag = DAG(
    "exchangerate",
    default_args=default_args,
    schedule_interval=timedelta(hours=3),
    catchup=False
)


def do_work():
    url = 'https://api.exchangerate.host/latest'
    response = requests.get(url)
    data = response.json()

    print(data)


with airflow_dag:
    PythonOperator(
        task_id="get_exchangerate_data",
        python_callable=do_work
    )
