import os
import sys
import logging
import json
import boto3
import psycopg2
from decimal import Decimal


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.StreamHandler(stream=sys.stdout)   # for lambda
fh_formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(filename)s,%(funcName)s,%(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)


BUCKET_NAME = 'sakurai-test-s3'
S3PREFIX = f's3://{BUCKET_NAME}/'
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)


connection_config = {
    'user': 'postgres',
    'password': 'TearBirds0',
    'host': 'sakurai-database-1.cneg46zalaof.ap-northeast-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'aichi'
}

def exist_file(path):
    objs = bucket.meta.client.list_objects_v2(Bucket=bucket.name, Prefix=path)
    if objs.get('Contents'):
        if len(objs['Contents']) > 0:
            return True
        else:
            logger.error('unknown {}'.format(path))
    else:
        logger.error('not found {}'.format(path))
    return False

    
    
def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    print(event)
    print(context)

    name = event['queryStringParameters']['name']

    path = os.path.join('pdfs', f'{name}.pdf')

    rows = []
    with psycopg2.connect(**connection_config) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT "地域名","市区町村名","総人口","男","女" FROM population WHERE "地域名"=' + "'" + name + "'")
            rows = cur.fetchall()

    ret = {}
    ret['pdf_is_exist'] = exist_file(path)
    ret['data'] = [{'地域名': x[0], '市区町村名': x[1], '総人口': x[2], '男性人口': x[3], '女性人口': x[4]} for x in rows]

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(ret, default=decimal_default_proc)
    }