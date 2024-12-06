from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os,requests
import pandas as pd
from Data_Extract import clean_data_extract


dag_owner = 'ProjectIE'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }

with DAG(dag_id='Extract_data_into_Postgres',
        default_args=default_args,
        description='Extract into Postgres DB',
        start_date=datetime(2024,11,7),
        schedule_interval=None,
        catchup=False,
        tags=['']
)as dag:

    PostgresOperator_task_economy = PostgresOperator(
        task_id='PostgresOperator_task_economy',
        postgres_conn_id='postgres_connect_Project',
        sql = 'sql/economy_flight.sql',
    )
    PostgresOperator_task_business = PostgresOperator(
        task_id='PostgresOperator_task_business',
        postgres_conn_id='postgres_connect_Project',
        sql = 'sql/business_flight.sql',
    )
    PostgresOperator_task_cleandata = PostgresOperator(
        task_id='PostgresOperator_task_cleandata',
        postgres_conn_id='postgres_connect_Project',
        sql = 'sql/cleandata_flight.sql',
    )

    python_clean_data_extract = PythonOperator(
        task_id='Clean-Data-Extract',
        python_callable=clean_data_extract,
    )

    @task
    def insert_data_economy():
        data_path_economy = '/tmp/economy.csv'
        postgres_hook = PostgresHook(postgres_conn_id='postgres_connect_Project')
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        with open(data_path_economy, "r") as file:
            cur.copy_expert(
                "COPY economic_flight FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                file,
            )
        conn.commit()

    @task
    def insert_data_business():
        data_path_business = '/tmp/business.csv'
        postgres_hook = PostgresHook(postgres_conn_id='postgres_connect_Project')
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        with open(data_path_business, "r") as file:
            cur.copy_expert(
                "COPY business_flight FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                file,
            )
        conn.commit()
    

[PostgresOperator_task_economy, PostgresOperator_task_business, PostgresOperator_task_cleandata] >> python_clean_data_extract >> insert_data_economy() >> insert_data_business()