from airflow.hooks.postgres_hook import PostgresHook
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
        #         self.log.info('StageToRedshiftOperator not implemented yet')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(self.redshift_conn_id)
        redshift_hook.run(self.create_stmt.format(credentials.access_key, credentials.secret_key))
