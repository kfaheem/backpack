from datetime import datetime, timedelta
import os
import pandas as pd
import logging
import sys
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from etl import get_covid_data
from sql_queries import drop_query, create_query

# logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_path = "{}/covid_data.csv".format(os.getcwd())
data_location = "https://healthdata.gov/data.json"


def insert_data(filepath):
    """

    :param filepath:
    :return:
    """
    try:
        postgres_hook = PostgresHook("redshift")

        table_columns = ['@type', 'accessLevel', 'bureauCode', 'description', 'distribution',
                         'identifier', 'issued', 'keyword', 'landingPage', 'modified',
                         'programCode', 'theme', 'title', 'contactPoint.fn',
                         'contactPoint.hasEmail', 'publisher.@type', 'publisher.name',
                         'describedBy', 'references', 'accrualPeriodicity', 'temporal',
                         'dataQuality', 'license', 'describedByType', 'rights', 'language']

        df1 = pd.read_csv(filepath)

        insert_query = """INSERT INTO covid_data_tb ({}) VALUES ({})
        """.format(",".join(table_columns), "%s, " * 26)

        for i, row in df1.iterrows():
            postgres_hook.run(insert_query, row)

    except Exception as exception:
        logger.error("Received Exception in create_tables function - {}".format(exception))
        raise exception


def data_check():
    """

    :return:
    """
    try:
        postgres_hook = PostgresHook("redshift")
        select_query = "SELECT keyword FROM covid_data_tb LIMIT 10"
        postgres_hook.run(select_query)

    except Exception as exception:
        logger.error("Received Exception in data_check function - {}".format(exception))
        raise exception


default_args = {
    'owner': 'Brijesh Goharia',
    'start_date': datetime.now(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': True,
    'email_on_retry': False
}

dag = DAG(
    'Airflow_etl',
    default_args=default_args,
    schedule_interval="@daily"
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

save_covid_data_task = PythonOperator(
    task_id='save_data_from_source_to_local',
    dag=dag,
    python_callable=get_covid_data(data_location, file_path)
)

drop_table_task = PostgresOperator(
    task_id="drop_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=drop_query
)

create_table_task = PostgresOperator(
    task_id="create_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=create_query
)

insert_data_task = PythonOperator(
    task_id='insert_data',
    dag=dag,
    python_callable=insert_data(file_path)
)

data_check_task = PythonOperator(
    task_id='data_check',
    dag=dag,
    python_callable=data_check()
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> save_covid_data_task >> drop_table_task >> create_table_task >> insert_data_task >> data_check_task >> end_operator
