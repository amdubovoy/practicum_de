-- create airflow database and role

create database "airflow";
create user airflow with password 'airflow';
grant all privileges on database "airflow" to airflow;

-- create role and database for loading data

create database "data";
create user loader with password 'loader';
grant all privileges on database "data" to loader;
\connect "data";
create schema "data";
grant usage on schema "data" to loader;

-- create table for exchangerate data

create table if not exists "data"."data".exchangerate
(
    etl_ts          timestamp without time zone,
    currency_pair   varchar(10),
    rate            decimal(40, 2)
);
alter table "data".exchangerate owner to loader;
