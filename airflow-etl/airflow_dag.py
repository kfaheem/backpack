from datetime import datetime
import os

from airflow import DAG
# from airflow.contrib.hooks.aws_hook import AwsHook
# from airflow.hooks.postgres_hook import PostgresHook
# from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

from etl import get_covid_data

print(type(get_covid_data))
print(callable(get_covid_data))
file_path = "{}/covid_data.json".format(os.getcwd())
data_location = "https://healthdata.gov/data.json"

dag = DAG(
    'Airflow_etl',
    start_date=datetime.now()
)

save_data_task = PythonOperator(
    task_id='save_data_from_source_to_local',
    dag=dag,
    python_callable=get_covid_data(data_location, file_path)
)

# def load_data_to_redshift(*args, **kwargs):
#     aws_hook = AwsHook("aws_credentials")
#     credentials = aws_hook.get_credentials()
#     redshift_hook = PostgresHook("redshift")
#     redshift_hook.run(sql.COPY_ALL_TRIPS_SQL.format(credentials.access_key, credentials.secret_key))
#
#
#
#
# create_table = PostgresOperator(
#     task_id="create_table",
#     dag=dag,
#     postgres_conn_id="redshift",
#     sql=sql_statements.CREATE_TRIPS_TABLE_SQL
# )
#
# copy_task = PythonOperator(
#     task_id='load_from_s3_to_redshift',
#     dag=dag,
#     python_callable=load_data_to_redshift
# )
#
# location_traffic_task = PostgresOperator(
#     task_id="calculate_location_traffic",
#     dag=dag,
#     postgres_conn_id="redshift",
#     sql=sql_statements.LOCATION_TRAFFIC_SQL
# )
#
# create_table >> copy_task
# copy_task >> location_traffic_task

# https://github.com/apache/airflow/tree/master/airflow/contrib