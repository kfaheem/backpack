
# boto ===========================================

import boto3
from botocore.exceptions import ClientError

boto_session = boto3.session.Session(profile_name="")
credentials = boto_session.get_credentials()

aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
aws_session_token = credentials.token

# examples
s3_client = boto3.client('s3', aws_access_key_id=credentials.access_key,
                         aws_secret_access_key=credentials.secret_key,
                         aws_session_token=credentials.token,
                         region_name="")

# ===========================================


# elasticsearch ===========================================

from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers


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

# ===========================================

# sts ===========================================
sts_client = boto3.client('sts')

sts_assume_role_creds = sts_client.assume_role(RoleArn="", RoleSessionName="")
session_id = sts_assume_role_creds.get("Credentials").get("AccessKeyId")
session_key = sts_assume_role_creds.get("Credentials").get("SecretAccessKey")
session_token = sts_assume_role_creds.get("Credentials").get("SessionToken")

# Besides getting credentials from boto session, you can also use the credentials from sts assume role, as seen above,
# to establish boto clients.

# ===========================================
