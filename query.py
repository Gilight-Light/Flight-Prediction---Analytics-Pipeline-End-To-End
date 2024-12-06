import psycopg2
import pandas as pd

host = "localhost"         
port = "5435"              
database = "airflow" 
user = "airflow"     
password = "airflow" 

def query():
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Sucess to connect Database!")

        # Thực thi truy vấn và đưa dữ liệu vào DataFrame
        query = "SELECT * FROM cleandata_flight;"  # Thay 'your_table_name' bằng tên bảng của bạn
        df = pd.read_sql_query(query, conn)

        # Hiển thị DataFrame
        print(df.head())

        # Đóng kết nối
        conn.close()
        print("Close connect Database.")
        return df
    except Exception as e:
        print("Failed to connect Database", e)