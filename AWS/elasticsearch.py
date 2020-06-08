import boto3
from botocore.exceptions import ClientError

from aws_requests_auth.aws_auth import AWSRequestsAuth

from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

boto_session = boto3.session.Session(profile_name="")
credentials = boto_session.get_credentials()

aws_auth = AWSRequestsAuth(
    aws_access_key=credentials.access_key,
    aws_secret_access_key=credentials.secret_key,
    aws_token=credentials.token,
    aws_region="",
    aws_host="",
    aws_service='es'
    )

es_client = Elasticsearch(
    hosts=[{"host": "", "port": 443}],
    http_auth=aws_auth,
    timeout=300,
    use_ssl=True,
    verify_certs=False,
    connection_class=RequestsHttpConnection
)

# es scroll ================================

body = ""
search_list = []
total_obj = 0
data = es_client.search(
    index="",
    scroll="5m",
    size=1000,
    body=body
)
for item in data["hits"]["hits"]:
    search_list.append(item)
scroll_id = data["_scroll_id"]
scroll_size = len(data["hits"]["hits"])
total_obj += scroll_size
logger.info("Total objects retrieved - {}".format(total_obj))

while scroll_size > 0:
    data = es_client.scroll(
        scroll_id=scroll_id,
        scroll='5m'
    )
    for item in data["hits"]["hits"]:
        search_list.append(item)
    scroll_id = data["_scroll_id"]
    scroll_size = len(data["hits"]["hits"])
    total_obj += scroll_size
    logger.info("Total objects retrieved - {}".format(total_obj))

# ================================

# elasticsearch query examples ================================

query1 = {
    "_source": ["field1", "field2"],
    "query": {
        "bool": {
            "must": [
                {
                    "match": {"some_field": "some_value"}
                },
                {
                    "range": {
                        "time_field": {
                            "lt": "less than timestamp value",
                            "gte": "greater than equals timestamp value"
                        }
                    }
                }
            ]
        }
    },
    "sort": [
        {
            "time_field": "desc"
        }
    ],
    "aggs": {
        "some_field_name": {
            "cardinality": {
                "field(keyword 'field' & not a substitute)": "some_field_name"
            }
        }
    }
}

query2 = {
    "query": {
        "bool": {
            "must": [
                {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "some_field": "some_value"
                                }
                            },
                            {
                                "match": {
                                    "some_field": "some_value"
                                }
                            },
                            {
                                "match_phrase": {
                                    "some_field": "some_value"
                                }
                            }
                        ]
                    }
                },
                {
                    "range": {
                        "time_field": {
                            "lt": "less than timestamp value",
                            "gte": "greater than equals timestamp value"
                        }
                    }
                }
            ],
            "must_not": {
                "exists": {
                    "field(not a substitute)": "some_field_name"
                }
            }
        },
        "sort": [
            {
                "some_time_field": "desc"
            }
        ]
    }
}

# ================================

# es bulk ================================

doc_list = []


def gendata(some_docs_list):
    for item in some_docs_list:
        yield {
            "op_type": "update",
            "_index": "index_name",
            "_type": "document",
            "_id": "some unique id, if not passed assigned a randome value",
            "doc": item,
            "doc_as_upsert": True
        }


bulk_upload = helpers.bulk(es_client, gendata(some_docs_list=doc_list))

# ================================

