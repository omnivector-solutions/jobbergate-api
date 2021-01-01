"""
Put common s3 settings and hacks in one place
"""
import boto3
from botocore.client import Config


S3_CONFIG = Config(
    connect_timeout=25,
    retries={"max_attempts": 0},
)


def make_s3_client(bucket):
    """
    S3 client factory; standardize all our code on the same s3 settings

    Also hardcodes the bucket into the endpoint_url, so a particular client can only access
    this one bucket.

    This is a necessary hack due to the fact that boto3 gives us the wrong endpoint for eu-north-1 buckets.
    """
    return boto3.client("s3", config=S3_CONFIG)
