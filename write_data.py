import sys
import logging
import json
import redshift
import s3

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776


def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)


class ChunkWriter:
    def __init__(self, schema_name=redshift.OUTPUT_TABLE_SCHEMA,
                 table_name=redshift.OUTPUT_TABLE_NAME, chunk_size=10*MB):
        self.chunk_processed_size = 0
        self.target_chunk_size = chunk_size
        self.schema_name = schema_name
        self.table_name = table_name

        self.full_table_name = '-'.join([schema_name, table_name])

    def __enter__(self):
        self.output = self.open_s3()
        return self

    def __exit__(self, type, value, traceback):
        self.flush()

    def open_s3(self):
        self.s3_url = s3.get_chunk_file_url(self.full_table_name)
        return s3.open(self.s3_url)

    def write(self, record):
        if self.chunk_processed_size > self.target_chunk_size:
            self.flush()

        outstring = json.dumps(record) + '\n'
        outsize = sys.getsizeof(outstring)
        self.chunk_processed_size = self.chunk_processed_size + outsize
        self.output.write(outstring)

    def flush(self):
        self.output.close()

        logger.info("Loading chunk of size {}"
                    .format(humanbytes(self.chunk_processed_size)))

        redshift.copy(self.schema_name, self.table_name, self.s3_url)

        self.output = self.open_s3()
        self.chunk_processed_size = 0
