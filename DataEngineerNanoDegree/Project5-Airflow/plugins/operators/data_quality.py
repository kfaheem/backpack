from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_conn_id, tables,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.tables = tables

    def execute(self, context):

        tables = self.tables
        redshift_hook = PostgresHook("redshift")
        for table in tables:
            self.log.info("Conducting Quality Check for table {}".format(table))

            records = redshift_hook.get_records("SELECT COUNT(*) FROM {}".format(table))
            condition_a = len(records) < 1
            condition_b = len(records[0]) < 1
            condition_c = records[0][0] < 1
            if condition_a or condition_b:
                raise ValueError("Data quality check failed for {} returned no results".format(table))

            if condition_c:
                raise ValueError("Data quality check failed for {}.".format(table))

            if not condition_a and not condition_b and not condition_c:
                self.log.info("Data quality check passed for table {}".format(table))
