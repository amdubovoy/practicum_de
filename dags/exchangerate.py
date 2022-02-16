import datetime
from datetime import timedelta

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago


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


def do_work(**ctx):
    query = "select exists(select 1 from data.exchangerate);"
    data_present = PostgresHook(postgres_conn_id="pg").get_first(query)[0]

    if not data_present:
        url = "https://api.exchangerate.host/timeseries"
        params = dict(
            start_date="2020-01-01",
            end_date=ctx["ds"],
            base="BTC",
            symbols="USD",
        )
        response = requests.get(url, params=params)
        data = response.json()

        result = []
        for date, rate in data.get("rates", {}).items():
            result.append(
                (
                    datetime.date(*(int(s) for s in date.split("-"))),
                    "BTC/USD",
                    float(rate.get("USD")),
                )
            )
    else:
        url = "https://api.exchangerate.host/latest"

        params = dict(
            base="BTC",
            symbols="USD"
        )
        etl_ts = datetime.datetime.utcnow()
        response = requests.get(url, params=params)
        data = response.json()

        result = [
            (
                etl_ts,
                "BTC/USD",
                float(data.get("rates", {}).get("USD")),
            )
        ]

    PostgresHook(postgres_conn_id="pg").insert_rows(
        "data.exchangerate",
        result,
        ["etl_ts", "currency_pair", "rate"],
    )


with airflow_dag:
    PythonOperator(
        task_id="get_exchangerate_data",
        python_callable=do_work
    )
