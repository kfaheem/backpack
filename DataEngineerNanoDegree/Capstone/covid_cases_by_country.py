import requests
import pandas as pd
import json
import logging
import sys
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers

# logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_countries(api_endpoint):
    """
    I hit the covid19api endpoint which returns all the country names for which covid data is available
    :param api_endpoint: str - "https://api.covid19api.com/countries"
    :return: list - A list of dictionaries. [{"Country Name": "United States", Slug": "united-states", "ISO2":"US"},
    {}, ..., {}]
    """
    try:
        response = requests.get(api_endpoint)
        logger.info("Response Status Code for Countries API endpoint - {}".format(response.status_code))

        response_list = json.loads(response.text)
        logger.info("Number of Country Records received - {}".format(len(response_list)))
        print(response_list)
        return response_list

    except Exception as exception:
        logger.error("Received Exception in get_countries function "
                     "in covid_cases_by_country.py - {}".format(exception))
        raise exception


def get_unique_countries(countries):
    """
    I filter a list of dictionaries containing Country Names by converting the list to a Pandas Dataframe
    and dropping duplicate Country Names
    :param countries: list - A list of dictionaries as obtained from the get_countries function
    :return: list - A list of dictionaries. [{"Country Name": "United States", Slug": "united-states", "ISO2":"US"},
    {}, ..., {}]
    """
    try:
        df = pd.DataFrame(countries)
        logger.info("Original Countries DF Shape - {}".format(df.shape))

        unique_df = df.drop_duplicates(subset="Country Name")
        logger.info("Unique Countries DF Shape - {}".format(unique_df.shape))

        return unique_df.to_dict(orient="records")

    except Exception as exception:
        logger.error("Received Exception in get_unique_countries function "
                     "in covid_cases_by_country.py - {}".format(exception))
        raise exception


def covid_by_country(countries):
    """
    I hit the covid19api endpoint for each country and return the available covid data
    :param countries: list - a List of dictionaries including Country Names as obtained from the
    get_unique_countries function.
    :return: tuple - list_a, list_b.
    list_a - [{"Country": "Switzerland", "CountryCode": "CH", "Lat": "46.82", "Lon": "8.23", "Cases": 1,
    "Status": "confirmed", "Date": "2020-02-25T00:00:00Z"}, {}, ..., {}]
    list_b - [{"Slug": "united-states", "Count":"244500"}, {}, ..., {}]
    """
    try:
        covid_cases = []
        record_counts = []

        for i, country in enumerate(countries):
            country_slug = country.get("Slug")

            logger.info("Collecting data for country {} - {}/{}".format(country_slug, i + 1, len(countries)))

            url = "https://api.covid19api.com/dayone/country/{}".format(country_slug)

            response = requests.get(url)
            logger.info("Response Status Code for country {} - {}".format(country_slug, response.status_code))

            response_list = json.loads(response.text)
            logger.info("Record count for {} - {}".format(country_slug, len(response_list)))

            record_counts.append({
                "Slug": country_slug, "Count": len(response_list)
            })

            covid_cases += response_list

        return covid_cases, record_counts

    except Exception as exception:
        logger.error("Received Exception in covid_by_country function "
                     "in covid_cases_by_country.py - {}".format(exception))
        raise exception


def generate_es_data(covid_response):
    """
    I generate dictionary objects for each document to be posted to Elasticsearch.
    :param covid_response: list - A list of dictionaries obtained from the covid_by_country function.
    :return: yield a collection of dictionary objects
    """
    try:
        for item in covid_response:

            date = str(item.get("Date")).replace(":", "-")
            country_code = item.get("CountryCode")
            _id = "{}/{}".format(country_code, date)

            yield {
                "op_type": "update",
                "_index": "covid_by_country",
                "_type": "_doc",
                "_id": _id,
                "doc": item,
                "doc_as_upsert": True
            }

    except Exception as exception:
        logger.error("Received Exception in generate_es_data function "
                     "in covid_cases_by_country.py - {}".format(exception))
        raise exception


def main():
    """
    I hit the covid19api at two different endpoints. The first endpoint returns all the countires for which covid
    data is available. I use the country names to then hit the second endpoint which returns covid data for the
    given country for each day available.
    :return:
    """
    try:
        countries_api_endpoint = "https://api.covid19api.com/countries"
        countries = get_countries(api_endpoint=countries_api_endpoint)

        unique_countries = get_unique_countries(countries)

        covid_response = covid_by_country(countries=unique_countries)

        if covid_response:
            es_client = Elasticsearch(
                hosts=[{"host": "", "port": 443}],
                timeout=300,
                use_ssl=True,
                verify_certs=False,
                connection_class=RequestsHttpConnection
            )

            es_bulk = helpers.bulk(es_client, generate_es_data(covid_response[0]))

            logger.info("es_bulk response - {}".format(es_bulk))

        else:
            logger.warning("No Covid Response found")

    except Exception as exception:
        logger.error("Received Exception in main function "
                     "in covid_cases_by_country.py - {}".format(exception))


if __name__ == "__main__":
    main()
