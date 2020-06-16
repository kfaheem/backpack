from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self, redshift_conn_id, table, create_stmt,
                 sql_query,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id,
        self.sql_query = sql_query
        self.create_stmt = create_stmt
        self.table = table

    def execute(self, context):

        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Deleting Redshift table {} if it exists".format(self.table))
        delete_query = "DROP TABLE IF EXISTS {}".format(self.table)
        redshift_hook.run(delete_query)

        self.log.info("Creating Redshift table {}".format(self.table))
        redshift_hook.run(self.create_stmt)

        self.log.info("Inserting data into Redshift table {}".format(self.table))
        redshift_hook.run(self.sql_query)
