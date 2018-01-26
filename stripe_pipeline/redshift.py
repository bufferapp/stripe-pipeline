import os
from retrying import retry
from random import randint
from sqlalchemy import create_engine
import s3

OUTPUT_TABLE_NAME = 'subscription_events'
OUTPUT_TABLE_SCHEMA = 'buda_stripe'
MIN_RETRY_WAIT = 1000*30
MAX_RETRY_WAIT = MIN_RETRY_WAIT*3
MAX_RETRY_ATTEMPTS = 10


def get_engine():
    redshift_db_name = os.getenv('REDSHIFT_DB_NAME')
    redshift_user = os.getenv('REDSHIFT_USER')
    redshift_password = os.getenv('REDSHIFT_PASSWORD')
    redshift_endpoint = os.getenv('REDSHIFT_ENDPOINT')
    redshift_db_port = int(os.getenv('REDSHIFT_DB_PORT'), 0)

    engine_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        redshift_user, redshift_password, redshift_endpoint,
        redshift_db_port, redshift_db_name)

    return create_engine(engine_string)


@retry(wait_random_min=MIN_RETRY_WAIT, wait_random_max=MAX_RETRY_WAIT,
       stop_max_attempt_number=MAX_RETRY_ATTEMPTS)
def copy(schema_name, table_name, s3_url):
    creds = 'aws_access_key_id={};aws_secret_access_key={}'.format(
        s3.env['s3_access_key'],
        s3.env['s3_secret_key']
    )

    nonce = str(randint(1, 10**20))
    staging_table = '#{schema_name}_{table_name}_{nonce}'.format(**locals())
    full_table_name = '{schema_name}.{table_name}'.format(**locals())

    lock_stmt = "lock {full_table_name}".format(**locals())

    create_stg = ("create table {staging_table}"
                  "(like {full_table_name});".format(**locals()))

    copy_stmt = ("copy {staging_table} from '{s3_url}' "
                 "credentials '{creds}' "
                 "acceptinvchars '.' format as json 'auto'"
                 .format(**locals()))

    delete_stmt = ("delete from {full_table_name} "
                   "where id in "
                   "(select id from {staging_table});"
                   .format(**locals()))

    insert_stmt = ("insert into {full_table_name}"
                   "(select * from {staging_table});".format(**locals()))

    queue = [lock_stmt, create_stg, copy_stmt, delete_stmt, insert_stmt]
    sa_engine = get_engine()
    with sa_engine.begin() as con:
        for stmt in queue:
            con.execute(stmt)


def get_latest_timestamp():
        query = 'select max(created_at) from {}.{}'.format(
            OUTPUT_TABLE_SCHEMA, OUTPUT_TABLE_NAME)
        engine = get_engine()
        result = engine.execute(query)
        return list(result)[0][0]
