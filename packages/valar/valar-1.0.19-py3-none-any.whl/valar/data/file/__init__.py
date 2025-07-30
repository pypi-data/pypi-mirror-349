import json
from io import BytesIO

from django.conf import settings
from minio import Minio
from urllib3 import HTTPResponse

def minio_upload_object(bucket_name, object_name, _bytes):
    client = __get_minio_client__()
    __create_bucket__(bucket_name, client)
    file_data = BytesIO(_bytes)
    file_size = len(_bytes)  # file.siz
    client.put_object(bucket_name=bucket_name, object_name=object_name, data=file_data, length=file_size)
    return f'{bucket_name}/{object_name}'

def minio_remove_object(bucket_name, object_name):
    client = __get_minio_client__()
    client.remove_object(bucket_name=bucket_name, object_name=object_name)

def minio_remove_path(path):
    [bucket_name, object_name] = path.split('/')
    client = __get_minio_client__()
    client.remove_object(bucket_name=bucket_name, object_name=object_name)


def minio_read_object(bucket_name, object_name) -> HTTPResponse:
    client = __get_minio_client__()
    return client.get_object(bucket_name=bucket_name, object_name=object_name)





def __get_minio_client__(bucket_name=None):
    options = settings.MINIO_SETTINGS
    client =  Minio(**options)
    if bucket_name:
        __create_bucket__(bucket_name, client)
    return client

def __create_bucket__(bucket_name, client=None):
    client = client or __get_minio_client__()
    exists = client.bucket_exists(bucket_name)
    if not exists:
        client.make_bucket(bucket_name)
        policy = generate_policy(bucket_name)
        client.set_bucket_policy(bucket_name, policy)


def get_minio_bucket_name(entity):
    value = f'{settings.BASE_DIR.name}.{entity}'
    bucket_name = value.replace('_','-').lower()
    __create_bucket__(bucket_name)
    return bucket_name

def get_minio_object_name(_id, prop, file_name):
    return f"{_id}-{prop}-{file_name}"

def generate_policy(bucket_name):
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetBucketLocation",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            },
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
      ]})
