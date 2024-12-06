from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os,requests
import pandas as pd
# from Data_Transformation import Data_Transformation
import numpy as np


dag_owner = 'ProjectIE'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }

with DAG(dag_id='ETL_DATA',
        default_args=default_args,
        description='ETL data from DB, load into DB Postgres',
        start_date=datetime(2024,11,7),
        schedule_interval=None,
        catchup=False,
        tags=['']
)as dag:
    @task()
    def get_data_as_df(table):
        try:
        # Kết nối đến PostgreSQL
            pg_hook = PostgresHook(postgres_conn_id='postgres_connect_Project')

            # Truy vấn dữ liệu và chuyển thành DataFrame
            query = f"SELECT * FROM {table}"  # Cần cẩn thận nếu `table` chứa ký tự đặc biệt
            print(f"Thực thi truy vấn: {query}")
            df = pg_hook.get_pandas_df(query)

            return df
        
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu từ bảng {table}: {e}")
            raise

    # @task()
    # def df_to_postgres_direct(df, table_name):
    #     try:
    #         # Kết nối đến PostgreSQL
    #         pg_hook = PostgresHook(postgres_conn_id='postgres_connect_Project')
    #         engine = pg_hook.get_sqlalchemy_engine()

    #         # Tải DataFrame lên PostgreSQL
    #         df.to_sql(
    #             name=table_name,
    #             con=engine,
    #             if_exists='append',  # Lựa chọn: 'append', 'replace', hoặc 'fail'
    #             index=False,  # Không ghi cột index của DataFrame vào bảng
    #             method='multi'  # Tối ưu hóa bằng cách chèn nhiều dòng cùng lúc
    #         )
    #         print(f"Dữ liệu đã được tải lên thành công vào bảng {table_name}")
    #     except Exception as e:
    #         print(f"Đã xảy ra lỗi khi tải dữ liệu vào bảng {table_name}: {e}")
    #         raise  # Ném lại lỗi để đảm bảo DAG của Airflow không bị lầm tưởng là chạy thành công
    @task()
    def Data_Transformation(read_economy, read_business):
        def convert_to_hours(time_str):
            hours, minutes = 0, 0
            if 'h' in time_str and time_str.split('h')[0].strip() != '':
                hours = float(time_str.split('h')[0].strip())
            if 'm' in time_str and time_str.split('h')[1].replace('m', '').strip() != '':
                minutes = float(time_str.split('h')[1].replace('m', '').strip())
            return hours + minutes / 60

        def categorize_time(time):
            hour = time.hour
            if 0 <= hour < 4:
                return 'Late_Night'
            elif 4 <= hour < 8:
                return 'Early_Morning'
            elif 8 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 16:
                return 'Afternoon'
            elif 16 <= hour < 20:
                return 'Evening'
            else:
                return 'Night'
            
        def get_stops(stop_value):
            if stop_value == 'non-stop':
                return 'zero'
            elif stop_value == '1-stop':
                return 'one'
            else:
                return 'two_or_more'



        ## Create list collumn ELT
        columns_to_keep = ['date', 'airline', 'flight', 'source_city', \
                        'departure_time', 'stops', 'arrival_time', 'destination_city', \
                        'class', 'duration', 'days_left', 'price']

        ## Data Transform
        df_combined = pd.concat([read_economy, read_business], axis=0, ignore_index=True)
        df_combined['stop'] = df_combined['stop'].str.replace(r'[\t"]', '', regex=True)
        df_combined['stop'] = df_combined['stop'].str.replace(r'[\n"]', '', regex=True)
        df_combined['stop'] = df_combined['stop'].str.replace(' ', '', regex=True)
        df_combined['hours'] = df_combined['time_taken'].apply(convert_to_hours)
        df_combined['days_left'] = (df_combined['hours'] // 24 + 1).astype(int)
        df_combined['duration'] = df_combined['hours'].round(2)
        df_combined['flight'] = df_combined['ch_code'] + '-'  + df_combined['num_code'].astype(str)
        df_combined.rename(columns={'from': 'source_city', 'to': 'destination_city'}, inplace=True)
        df_combined['arr_time'] = pd.to_datetime(df_combined['arr_time'], format='%H:%M')
        df_combined['arrival_time'] = df_combined['arr_time'].apply(categorize_time)
        df_combined['dep_time'] = pd.to_datetime(df_combined['dep_time'], format='%H:%M')
        df_combined['departure_time'] = df_combined['dep_time'].apply(categorize_time)
        df_combined['stops'] = df_combined['stop'].astype(str).apply(get_stops)
        df_selected = df_combined[columns_to_keep]
        df_selected['date'] = pd.to_datetime(df_selected['date'], format='%d-%m-%Y')

        ## Get Gold Data
        df_sorted = df_selected.sort_values(by='date',ascending=True)
        print(df_sorted.head())
        return df_sorted

    @task()
    def Extract_into_DB(df_gold):
    
        pg_hook = PostgresHook(postgres_conn_id='postgres_connect_Project')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        df_gold_tuples = list(df_gold.itertuples(index=False, name=None))
        try:
            insert_query = """
                INSERT INTO cleandata_flight (date, airline, flight, source_city, departure_time, stops, arrival_time, destination_city, class, duration, days_left, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            cursor.executemany(insert_query, df_gold_tuples)
            conn.commit()
            cursor.close()
            print("Success ETL DATA INTO POSTGREDB !!!")
        except Exception as e:
            print(f"Error push Data into table cleandata_flight: {e}")
            raise
    
    @task()
    def convert_golddata_to_csv(df_gold):
        data_dir = '/opt/airflow/data'
        os.makedirs(data_dir, exist_ok=True)
        df_gold.to_csv(f"{data_dir}/Clean_Dataset.csv", index=False)


## DAG Worflow- ETL Pipeline
    data_economic = get_data_as_df('economic_flight')
    data_business = get_data_as_df('business_flight')
    data_gold = Data_Transformation(data_economic, data_business)
    Extract_into_DB(data_gold)
    convert_golddata_to_csv(data_gold)
    
    