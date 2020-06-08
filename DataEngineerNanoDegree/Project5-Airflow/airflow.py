from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hello_world():
    logger.info("Hello World")


# Define a DAG
dag_1 = DAG("dag_1",
            start_date=datetime(2020, 6, 7),
            schedule_interval="@daily")  # @once, @hourly, @daily, @weekly, @monthly, @yearly, none

task_1 = PythonOperator(
    task_id="hello world",
    description="task for dag",
    python_callable=hello_world,
    dag=dag_1
)

# task_2
# if task_2 depends on task_1
# task_1 >> task_2