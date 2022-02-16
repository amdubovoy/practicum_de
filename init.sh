#!/usr/bin/env bash

# create meta-db
airflow db init
airflow db upgrade

# create admin user
airflow users create -e admin@admin.com -f admin -l admin -p admin -r Admin -u admin

# create pg connection
airflow connections add 'pg' --conn-type 'postgres' --conn-login 'loader' --conn-password 'loader' --conn-host 'postgres' --conn-port '5432' --conn-schema 'data'

# run airflow
airflow scheduler -D
airflow webserver
