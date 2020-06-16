import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def drop_tables(cur, conn):
    """
    I drop Redshift tables based on the queries provided in drop_table_queries. This function is run as a
    preventative measure before the create_tables function.
    :param cur: Redshift Database cursor object
    :param conn: Redshift Database connection object
    :return:
    """
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()

        return True

    except Exception as exception:
        logger.error("Received Exception in drop_tables function - {}".format(exception))
        raise exception


def create_tables(cur, conn):
    """
    I create Redshift tables based on the queries provided in create_table_queries
    :param cur: Redshift Database cursor object
    :param conn: Redshift Database connection object
    :return: True
    """
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()

        return True

    except Exception as exception:
        logger.error("Received Exception in create_tables function - {}".format(exception))
        raise exception


def main():
    """
    I connect to a Redshift database using parameters from dwh.cfg config file and drop & create the required tables
    for the ETL process.
    :return: True - if all tables are deleted and created successfully
    """
    try:

        config = configparser.ConfigParser()
        config.read('dwh.cfg')

        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()

        drop_tables(cur, conn)
        create_tables(cur, conn)

        conn.close()

        return True

    except Exception as exception:
        logger.error("Received Exception in main function - {}".format(exception))


if __name__ == "__main__":
    main()
