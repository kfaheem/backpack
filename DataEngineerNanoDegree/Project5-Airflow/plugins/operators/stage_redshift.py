from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, aws_credentials_id, redshift_conn_id,
                 s3_bucket, s3_key, table, create_stmt,
                 *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.aws_credentials_id = aws_credentials_id
        self.redshift_conn_id = redshift_conn_id,
        self.s3_bucket = s3_bucket,
        self.s3_key = s3_key,
        self.table = table,
        self.create_stmt = create_stmt

    def execute(self, context):

        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Deleting Redshift table {} if it exists".format(self.table))
        delete_query = "DROP TABLE IF EXISTS {}".format(self.table)
        redshift_hook.run(delete_query)

        self.log.info("Creating Redshift table {}".format(self.table))
        redshift_hook.run(self.create_stmt)

        self.log.info("Copying data from S3 to Redshift")
        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key)
        copy_query = """
        COPY {} FROM {} credentials 'aws_access_key_id={};aws_secret_access_key={}'
        """.format(self.table, s3_path, credentials.access_key,
                   credentials.secret_key)
        redshift_hook.run(copy_query)
