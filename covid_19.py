from bs4 import BeautifulSoup
import requests
import logging
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers
import sys

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_covid_data(URL):
    """

    :param URL:
    :return:
    """
    try:
        table_data = []

        logger.info("Executing Get Request")
        page = requests.get(URL)
        logger.info("Received Page Content")

        logger.info("Initiating Scraping for Page Content")
        soup = BeautifulSoup(page.content, 'html.parser')

        print(soup.prettify())
        # data_table = soup.find("table", attrs={"class": "waffle"})
        #
        # t_headers = ['Patient Number', 'State Patient Number', 'Date Announced', 'Age Bracket',
        #              'Gender', 'Detected City', 'Detected District', 'Detected State', 'State Code', 'Current Status',
        #              'Notes', 'Contracted from which Patient (Suspected)', 'Nationality', 'Type of transmission',
        #              'Status Change Date', 'Source_1', 'Source_2', 'Source_3', 'Backup Notes']
        #
        # for tr in data_table.tbody.find_all("tr"):
        #     t_row = {}
        #     for td, th in zip(tr.find_all("td"), t_headers):
        #         t_row[th] = td.text.replace('\n', '').strip()
        #     table_data.append(t_row)
        #
        # table_data.remove(table_data[0])
        # table_data.remove(table_data[0])
        logger.info("Scraping Complete")
        #
        # return table_data

    except Exception as exception:
        logger.error("Received Exception in get_covid_data function - {}".format(exception))
        raise exception


def yield_es_data(covid_data):
    """

    :param covid_data:
    :return:
    """
    try:
        for item in covid_data:
            yield {
                "op_type": "update",
                "_index": "covid-19-poc",
                "_type": "document",
                "doc": item,
                "doc_as_upsert": True
            }

    except Exception as exception:
        logger.error("Received Exception in yield_es_data function - {}".format(exception))
        raise exception


def main():
    """

    :return:
    """
    try:
        url = "https://www.mottchildren.org"

        covid_data = get_covid_data(URL=url)

        # es_client = Elasticsearch(
        #     hosts=[{"host": "", "port": 443}],
        #     timeout=300,
        #     use_ssl=True,
        #     verify_certs=False,
        #     connection_class=RequestsHttpConnection
        # )
        #
        # es_response = helpers.bulk(es_client, yield_es_data(covid_data=covid_data))
        # logger.info("es_response - {}".format(es_response))

    except Exception as exception:
        logger.error("Received Exception in main function - {}".format(exception))


if __name__ == "__main__":
    main()
