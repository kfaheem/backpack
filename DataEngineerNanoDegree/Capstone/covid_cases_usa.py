import requests
import pandas as pd
import json
import logging
import sys
import os
from glob import glob
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers

# logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_files_under_dir(dir_path):
    """
    I find all the files under the given directory
    :param dir_path: str - Directory Path
    :return: A list of file paths
    """
    try:
        files = glob(dir_path)
        logger.info("Found {} files under dir {}".format(len(files), dir_path))

        return files

    except Exception as exception:
        logger.error("Received Exception in get_files_under_dir function "
                     "in covid_cases_usa.py - {}".format(exception))
        raise exception


def create_df(file, df_type):
    """
    I read the given file into a Pandas Dataframe. The Dataframe is then massaged to add three new columns -
    reportTimestamp, dateId, confirmedCases/deaths to make the data concatenable and conducive to Elasticsearch
    :param file: str - Absolute File path
    :param df_type: str - the type of dataframe - confirmed/deaths, this determines which column should be added to
    the Dataframe.
    :return: Pandas Dataframe
    """
    try:
        date_id = file.split("/")[-1].split(".")[0]
        report_timestamp = datetime.strptime(date_id, "%m-%d-%y").strftime("%Y-%m-%dT%H:%M:%S")

        df = pd.read_csv(file)
        columns = df.columns.tolist()

        df["reportTimestamp"] = df.apply(lambda row: report_timestamp, axis=1)
        df["dateId"] = df.apply(lambda row: date_id, axis=1)

        if df_type == "confirmed":
            df["confirmedCases"] = df.apply(lambda row: row[columns[-1]], axis=1)
        else:
            df["deaths"] = df.apply(lambda row: row[columns[-1]], axis=1)

        df.drop(columns[-1], axis=1, inplace=True)

        return df

    except Exception as exception:
        logger.error("Received Exception in create_df function "
                     "in covid_cases_usa.py - {}".format(exception))
        raise exception


def concat_df(files, df_type):
    """
    I read all the files under the given location and concatenate each file into a Pandas Dataframe
    :param files: list - A list of file names
    :param df_type: str - the type of dataframe - confirmed/deaths
    :return: A list of dictionaries
    """
    try:
        all_dfs = []
        for i, file in enumerate(files):
            logger.info("Processing file {}/{}".format(i + 1, len(files)))

            df = create_df(file=file, df_type=df_type)
            all_dfs.append(df)

        logger.info("Total Number of DFs created - {}".format(len(all_dfs)))

        concatenated_df = pd.concat(all_dfs, axis=0)
        concatenated_df.reset_index(inplace=True)
        logger.info("concatenated_df Shape - {}".format(concatenated_df.shape))

        return concatenated_df.to_dict(orient="records")

    except Exception as exception:
        logger.error("Received Exception in concat_df function "
                     "in covid_cases_usa.py - {}".format(exception))
        raise exception


def merge_df(covid_df, population_df):
    """
    I merge the given dataframe (confirmed_cases_df/covid_deaths_df) with the population dataframe on the County
    Name column
    :param covid_df: Pandas df
    :param population_df: Pandas df
    :return: A list of dictionaries
    """
    try:
        logger.info("Covid DF Shape - {}".format(covid_df.shape))
        logger.info("Populcation DF Shape - {}".format(population_df.shape))

        merged_df = pd.merge(covid_df, population_df[["County Name", "population"]], on="County Name")

        logger.info("Merged DF Shape - {}".format(merged_df.shape))

        return merged_df.to_dict(orient="records")

    except Exception as exception:
        logger.error("Received Exception in merge_df function "
                     "in covid_cases_usa.py - {}".format(exception))
        raise exception


def generate_es_data(covid_data):
    """
    I generate dictionary objects for each document to be posted to Elasticsearch.
    :param covid_data: list - A list of dictionaries obtained from the merge_df function.
    :return:
    """
    try:
        for item in covid_data:
            county_name = item.get("County Name")
            date_id = item.get("dateId")
            _id = "{}/{}".format(county_name, date_id)

            yield {
                "op_type": "update",
                "_index": "covid_usa",
                "_type": "_doc",
                "_id": _id,
                "doc": item,
                "doc_as_upsert": True
            }

    except Exception as exception:
        logger.error("Received Exception in generate_es_data function "
                     "in covid_cases_usa.py - {}".format(exception))
        raise exception


def main():
    """
    I read confirmed_cases and covid_deaths data from the given locations and concatenate the data into
    their respective Pandas Dataframes. The Dataframes are then merged with a Population Dataframe to add
    population information. The two concatenated Dataframes are then sent to Elasticsearch using the Bulk API.
    :return:
    """
    try:
        # Switch the wokring directory to Capstone
        cwd = os.getcwd()

        # Assign directory paths
        confirmed_cases_dir = "{}/covid_county_data/confirmed_cases/*".format(cwd)
        covid_deaths_dir = "{}/covid_county_data/covid_deaths/*".format(cwd)

        # Get all data files
        confirmed_cases_files = get_files_under_dir(confirmed_cases_dir)
        covid_deaths_files = get_files_under_dir(covid_deaths_dir)

        # Concatenate Dataframes
        confirmed_cases_df = concat_df(files=confirmed_cases_files, df_type="confirmed")
        covid_deaths_df = concat_df(files=covid_deaths_files, df_type="deaths")

        # Merge populcation Dataframe
        population_df = pd.read_csv("{}/covid_county_data/county_population.csv".format(cwd))
        merged_confirmed_cases_df = merge_df(covid_df=confirmed_cases_df, population_df=population_df)
        merged_covid_deaths_df = merge_df(covid_df=covid_deaths_df, population_df=population_df)

        # Set Elasticsearch Client
        es_client = Elasticsearch(
            hosts=[{"host": "", "port": 443}],
            timeout=300,
            use_ssl=True,
            verify_certs=False,
            connection_class=RequestsHttpConnection
        )

        # Post data to Elasticsearch
        confirmed_cases_es_bulk = helpers.bulk(es_client, generate_es_data(covid_data=merged_confirmed_cases_df))
        logger.info("confirmed_cases_es_bulk response - {}".format(confirmed_cases_es_bulk))

        covid_deaths_es_bulk = helpers.bulk(es_client, generate_es_data(covid_data=merged_covid_deaths_df))
        logger.info("covid_deaths_es_bulk response - {}".format(covid_deaths_es_bulk))

    except Exception as exception:
        logger.error("Received Exception in main function "
                     "in covid_cases_usa.py - {}".format(exception))


if __name__ == "__main__":
    main()
