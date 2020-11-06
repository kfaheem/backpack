import pandas as pd
import requests
import sys
import logging
import os
import psycopg2

# logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_covid_data(data_location, file_path):
    """

    :param data_location:
    :param file_path:
    :return:
    """
    try:
        response = requests.get(data_location, verify=False)

        # Read all data into dataframe
        df1 = pd.DataFrame(response.json())

        # Normalize dataset column
        df2 = pd.json_normalize(df1["dataset"])

        logger.info("df2 original shape - {}".format(df2.shape))

        # drop rows from df2 not related to covid keywords
        covid_keywords = {"coronavirus", "covid", "covid-19"}

        for _, row in df2.iterrows():

            dataset_keywords = set(row["keyword"])

            subset = dataset_keywords.intersection(covid_keywords)

            # subset exists if dataset_keywords contain one or more covid_keywords
            if not subset:
                df2.drop(index=_, axis=0, inplace=True)

        logger.info("df2 new shape - {}".format(df2.shape))

        # save data locally
        df2.to_json(file_path)

        return True

    except Exception as exception:
        logger.error("Received exception in get_covid_data function - {}".format(exception))
        raise exception


def create_database():
    """
    - Creates and connects to the parent_db
    - Returns the connection and cursor to parent_db
    """
    try:

        # connect to default database
        conn = psycopg2.connect("host=127.0.0.1 dbname=parent_db user=student password=student")
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # create covid_data_db with UTF8 encoding
        cur.execute("DROP DATABASE IF EXISTS covid_data_db")
        cur.execute("CREATE DATABASE covid_data_db WITH ENCODING 'utf8' TEMPLATE template0")

        # close connection to parent database
        conn.close()

        # connect to covid_data_db
        conn = psycopg2.connect("host=127.0.0.1 dbname=covid_data_db user=student password=student")
        cur = conn.cursor()

        return cur, conn

    except Exception as exception:
        logger.error("Received exception in create_database function - {}".format(exception))
        raise exception


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    try:
        drop_query = "DROP TABLE IF EXISTS covid_data_tb"

        cur.execute(drop_query)
        conn.commit()

    except Exception as exception:
        logger.error("Received exception in drop_tables function - {}".format(exception))
        raise exception


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    try:
        table_columns = ['@type', 'accessLevel', 'bureauCode', 'description', 'distribution',
                         'identifier', 'issued', 'keyword', 'landingPage', 'modified',
                         'programCode', 'theme', 'title', 'contactPoint.fn',
                         'contactPoint.hasEmail', 'publisher.@type', 'publisher.name',
                         'describedBy', 'references', 'accrualPeriodicity', 'temporal',
                         'dataQuality', 'license', 'describedByType', 'rights', 'language']

        column_query = ["{} string".format(column_name) for column_name in table_columns]

        create_query = """CREATE TABLE IF NOT EXISTS covid_data_tb ({})""".format(", \n".join(column_query))

        cur.execute(create_query)
        conn.commit()

    except Exception as exception:
        logger.error("Received Exception in create_tables function - {}".format(exception))
        raise exception


def insert_data(cur, filepath):
    """

    :param cur:
    :param filepath:
    :return:
    """
    try:
        table_columns = ['@type', 'accessLevel', 'bureauCode', 'description', 'distribution',
                         'identifier', 'issued', 'keyword', 'landingPage', 'modified',
                         'programCode', 'theme', 'title', 'contactPoint.fn',
                         'contactPoint.hasEmail', 'publisher.@type', 'publisher.name',
                         'describedBy', 'references', 'accrualPeriodicity', 'temporal',
                         'dataQuality', 'license', 'describedByType', 'rights', 'language']

        df1 = pd.read_json(filepath)

        insert_query = """INSERT INTO covid_data_tb ({}) VALUES ({})
        """.format(",".join(table_columns), "%s, "*26)

        for i, row in df1.iterrows():
            cur.execute(insert_query, row)

    except Exception as exception:
        logger.error("Received Exception in create_tables function - {}".format(exception))
        raise exception


def data_check(cur):
    """

    :param cur:
    :return:
    """
    try:
        select_query = "SELECT * FROM covid_data_tb LIMIT 10"
        cur.execute(select_query)
        results = cur.fetchone()

        logger.info("Query Result - {}".format(results))

    except Exception as exception:
        logger.error("Received Exception in data_check function - {}".format(exception))
        raise exception


def main():
    """

    :return:
    """
    try:
        file_path = "{}/covid_data.json".format(os.getcwd())
        data_location = "https://healthdata.gov/data.json"

        # get, filter & save covid data
        get_covid_data(data_location, file_path)

        # create covid_data_db
        cur, conn = create_database()

        # drop & create covid_data_tb
        drop_tables(cur, conn)
        create_tables(cur, conn)

        # insert data into covid_data_tb
        insert_data(cur, file_path)

        # data check
        data_check(cur)

        conn.close()

    except Exception as exception:
        logger.error("Received exception in main function - {}".format(exception))


if __name__ == "__main__":
    main()
