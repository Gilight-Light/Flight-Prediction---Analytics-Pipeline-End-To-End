from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os,requests
import pandas as pd

dag_owner = 'ProjectIE'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }

with DAG(dag_id='Download_dataset_from_kaggle',
        default_args=default_args,
        description='Down load dataset from kaggle',
        start_date=datetime(2024,11,7),
        schedule_interval=None,
        catchup=False,
        tags=['']
)as dag:

    bash_task_down = BashOperator(
        task_id="Download_source_data_from_kaggle",
        bash_command='curl -L -o archive.zip https://www.kaggle.com/api/v1/datasets/download/shubhambathwal/flight-price-prediction',
        cwd = '/tmp',
    )
    
    bash_task_tar = BashOperator(
        task_id="bash_task_tar",
        bash_command='unzip archive.zip',
        cwd = '/tmp',
    )
