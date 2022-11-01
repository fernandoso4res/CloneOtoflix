from config import AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_URL
import boto3

def s3_client():
    return boto3.client('s3', endpoint_url=AWS_URL, region_name=AWS_DEFAULT_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def s3_resource():
    return boto3.resource('s3', endpoint_url=AWS_URL, region_name=AWS_DEFAULT_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def s3_bucket(bucket_name):
    s3 = s3_resource()
    return s3.Bucket(bucket_name)

def s3_object(bucket_name, key):
    s3 = s3_resource()
    return s3.Object(bucket_name, key)