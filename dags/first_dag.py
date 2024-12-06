from airflow import DAG
from airflow.decorators import task, dag

from datetime import datetime, timedelta 

dag_owner = 'dag_with_taskflow'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }

@dag(dag_id='dag_with_taskflow_v1',
     default_args = default_args,
     start_date = datetime(2024,10,29),
     schedule_interval='@daily')
def hello_world_elt():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Jerry',
            'last_name': 'Fridman'
        }
    @task()
    def get_age():
        return 19

    @task()
    def greet(first_name, last_name, age):
        print(f'Hello World! My name is {first_name} {last_name}'
              f'and I am {age} years old!')
    
    name = get_name()
    age = get_age()
    greet(name['first_name'], name['last_name'],age)

greet_dag = hello_world_elt()


    