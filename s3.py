import os
from datetime import datetime
from smart_open import smart_open

env = {
    's3_access_key': os.environ.get('AWS_ACCESS_KEY_ID'),
    's3_secret_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
    's3_root': os.getenv('REDSHIFT_COPY_S3_ROOT')
}


def get_chunk_file_url(full_table_name):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')
    path = '{full_table_name}/{timestamp}.json'.format(**locals())

    return get_url(path)


def get_url(path):
    fmt = {**env, **{'path': path}}
    url = 's3://{s3_root}/{path}'.format(**fmt)

    return url.format(**fmt)


def open(s3_url, mode='w', **kw):
    return smart_open(s3_url, mode, **kw)
