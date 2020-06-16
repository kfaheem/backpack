import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def load_staging_tables(cur, conn):
    """
    I load data from S3 into Redshift staging tables as mentioned in copy_table_queries
    :param cur: Redshift Database cursor object
    :param conn: Redshift Database connection object
    :return: True
    """
    try:
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()

        return True

    except Exception as exception:
        logger.error("Received Exception in load_staging_tables function - {}".format(exception))
        raise exception


def insert_tables(cur, conn):
    """
    I insert data from staging tables into fact & dimension tables.
    :param cur: Redshift Database cursor object
    :param conn: Redshift Database connection object
    :return:
    """
    try:
        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()

    except Exception as exception:
        logger.error("Received Exception in insert_tables function - {}".format(exception))
        raise exception


def main():
    """
    I connect to a Redshift database using parameters from dwh.cfg config file. I then load data from an S3 bucket
    into two staging tables and subsequently from the staging tables to fact & dimension tables.
    :return:
    """
    try:
        config = configparser.ConfigParser()
        config.read('dwh.cfg')

        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()

        load_staging_tables(cur, conn)
        insert_tables(cur, conn)

        conn.close()

    except Exception as exception:
        logger.error("Received Exception in main function - {}".format(exception))


if __name__ == "__main__":
    main()
