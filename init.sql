-- create airflow database and role

create database "airflow";
create user airflow with password 'airflow';
grant all privileges on database "airflow" to airflow;

-- create role and database for loading data

create database "data";
create user loader with password 'loader';
grant all privileges on database "data" to loader;
