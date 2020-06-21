import requests
import pandas as pd
import json
import logging
import sys

# logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_countries(api_endpoint):
    """

    :param api_endpoint:
    :return:
    """
    try:
        response = requests.get(api_endpoint)
        logger.info("Response Status Code for Countries API endpoint - {}".format(response.status_code))

        response_list = json.loads(response.text)
        logger.info("Number of Country Records received - {}".format(len(response_list)))

        return response_list

    except Exception as exception:
        logger.error("Received Exception in get_countries function "
                     "in covid_cases_by_country.py - {}".format(exception))
        raise exception


def get_unique_countries(countries):
    """

    :param countries:
    :return:
    """
    try:
        df = pd.DataFrame(countries)
        logger.info("Original Countries DF Shape - {}".format(df.shape))

        unique_df = df.drop_duplicates(subset="Country")
        logger.info("Unique Countries DF Shape - {}".format(unique_df.shape))

        return unique_df.to_dict(orient="records")

    except Exception as exception:
        logger.error("Received Exception in get_unique_countries function "
                     "in covid_cases_by_country.py - {}".format(exception))
        raise exception


def covid_by_country(countries):
    """

    :param countries:
    :return:
    """
    try:
        covid_cases = []
        record_counts = []

        for i, country in enumerate(countries):
            country_slug = country.get("Slug")

            logger.info("Collecting data for country {} - {}/{}".format(country_slug, i + 1, len(countries)))

            url = "https://api.covid19api.com/dayone/country/{}".format(country["Country"])

            response = requests.get(url)
            logger.info("Response Status Code for country {} - {}".format(country_slug, response.status_code))

            response_list = json.loads(response.text)
            logger.info("Record count for {} - {}".format(country["Country"], len(response_list)))

            record_counts.append({
                "Slug": country_slug, "Count": len(response_list)
            })

            covid_cases += response_list

        # df1 = pd.DataFrame(covid_cases)
        # df2 = pd.DataFrame(record_counts)

        print(type(covid_cases))
        print(type(record_counts))

        print(covid_cases)

        print(record_counts)
        # print(df1)
        # print(df1.columns)
        # print(df2)
        # print(df2["Count"].sum())
        return covid_cases, record_counts

    except Exception as exception:
        logger.error("Received Exception in covid_by_country function "
                     "in covid_cases_by_country.py - {}".format(exception))
        raise exception

# rez3 = requests.get("https://api.covid19api.com/world/total")

# print(rez3.text)

def main():
    """

    :return:
    """
    try:
        countries_api_endpoint = "https://api.covid19api.com/countries"
        countries = get_countries(api_endpoint=countries_api_endpoint)

        unique_countries = get_unique_countries(countries)

        covid_response = covid_by_country(countries=unique_countries)

    except Exception as exception:
        logger.error("Received Exception in main function "
                     "in covid_cases_by_country.py - {}".format(exception))


if __name__ == "__main__":
    main()
