import sys
from ext.storage import s3_bucket


def upload_fileobj(bucket_name, key, data):
    try:
        bucket = s3_bucket(bucket_name)
        bucket.upload_fileobj(data, key)
        return True
    except Exception as e:
        raise