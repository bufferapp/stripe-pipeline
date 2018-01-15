import os
from sqlalchemy import create_engine
import s3

OUTPUT_TABLE_NAME = 'subscription_events'
OUTPUT_TABLE_SCHEMA = 'buda_stripe'


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


def copy(schema_name, table_name, s3_url):
    creds = 'aws_access_key_id={};aws_secret_access_key={}'.format(
        s3.env['s3_access_key'],
        s3.env['s3_secret_key']
    )

    staging_table = '#{schema_name}_{table_name}'.format(**locals())
    full_table_name = '{schema_name}.{table_name}'.format(**locals())

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

    queue = [create_stg, copy_stmt, delete_stmt, insert_stmt]
    sa_engine = get_engine()
    with sa_engine.begin() as con:
        for stmt in queue:
            con.execute(stmt)
