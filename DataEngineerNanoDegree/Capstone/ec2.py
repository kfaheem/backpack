import boto3
from botocore.exceptions import ClientError
import sys
import logging
import csv
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers

# Set logger
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def read_s3(s3_client, bucket_name, bucket_key):
    """

    :param s3_client:
    :param bucket_name:
    :param bucket_key:
    :return:
    """
    try:
        response_list = []

        read_response = s3_client.get_object(Bucket=bucket_name, Key=bucket_key)

        response_status_code = read_response.get("ResponseMetadata").get("HTTPStatusCode")
        logger.info("Get Object response for Bucket {} & Key {} - {}".format(bucket_name, bucket_key,
                                                                             response_status_code))

        response_content = read_response.get("Body").read().decode("utf-8")

        content_list = response_content.split("\n")
        csv_dict_reader = csv.DictReader(content_list)
        for row in csv_dict_reader:
            response_list.append(dict(row))

        logger.info("Number of rows retrieved - {}".format(len(response_list)))

        return response_list

    except ClientError as err:
        logger.error("Received Client Error in read_s3 function - {}".format(err))
        raise err

    except Exception as exception:
        logger.error("Received Exception in read_s3 function - {}".format(exception))
        raise exception


def generate_es_data(response_list, es_index):
    """

    :param response_list:
    :param es_index:
    :return:
    """
    try:
        for item in response_list:
            yield {
                "_op_type": "update",
                "_index": es_index,
                "_type": "_doc",
                "doc": item,
                "doc_as_upsert": True
            }

    except Exception as exception:
        logger.error("Received Exception in generate_es_data function - {}".format(exception))
        raise exception


def main():
    """

    :return:
    """
    try:
        s3_client = boto3.client("s3")
        bucket_name = ""
        bucket_key = ""

        logger.info("Getting object {} from S3 bucket {}".format(bucket_key, bucket_name))

        s3_response = read_s3(s3_client=s3_client, bucket_name=bucket_name, bucket_key=bucket_key)

        if s3_response:

            es_index = ""

            es_client = Elasticsearch(
                hosts=[{"host": "", "port": 443}],
                timeout=300,
                use_ssl=True,
                verify_certs=False,
                connection_class=RequestsHttpConnection
            )

            es_bulk_response = helpers.bulk(es_client, generate_es_data(response_list=s3_response,
                                                                        es_index=es_index))

            logger.info("es_bulk_response - {}".format(es_bulk_response))

    except ClientError as err:
        logger.error("Received Client Error in main function - {}".format(err))

    except Exception as exception:
        logger.error("Received Exception in main function - {}".format(exception))

