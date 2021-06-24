import sys
sys.path.append('/var/runtime')

import json
import pandas as pd
import pdfkit
import boto3
import os
import psycopg2
from decimal import Decimal

s3 = boto3.resource('s3')

connection_config = {
    'user': 'postgres',
    'password': 'TearBirds0',
    'host': 'sakurai-database-1.cneg46zalaof.ap-northeast-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'aichi'
}

def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    print(event)
    print(context)

    name = event['queryStringParameters']['name']

    BUCKET_NAME = 'sakurai-test-s3'
    S3PREFIX = f's3://{BUCKET_NAME}/'
    TMP_DIR = '/tmp'
    lpath = os.path.join(TMP_DIR, f'{name}.pdf')
    path = os.path.join('pdfs', f'{name}.pdf')
    

    rows = []
    with psycopg2.connect(**connection_config) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT "地域名","市区町村名","総人口","男","女" FROM population WHERE "地域名"=' + "'" + name + "'")
            rows = cur.fetchall()

    data = [{'地域名': x[0], '市区町村名': x[1], '総人口': x[2], '男性人口': x[3], '女性人口': x[4]} for x in rows]
    
    data = {}
    data['地域名'] = [x[0] for x in rows]
    data['市区町村名'] = [x[1] for x in rows]
    data['総人口'] = [x[2] for x in rows]
    data['男性人口'] = [x[3] for x in rows]
    data['女性人口'] = [x[4] for x in rows]
    
    df = pd.DataFrame(data)

    table = df.to_html()
    html = '''
        <!DOCTYPE html>
        <html lang="ja">
        <head>
        <meta charset="utf-8">
        <title>test</title>
        </head>
        <body>
        {}
        </body>
        '''.format(table)
    pdfkit.from_string(html, lpath)

    bucket = s3.Bucket(BUCKET_NAME)
    print(lpath, ' -> ', path)
    try:
        bucket.upload_file(lpath, path, ExtraArgs={"ContentType": "application/pdf", 'ACL':'public-read'})
    except Exception as e:
        print(e)
        
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('OK')
    }
    

if __name__ == '__main__':
    print(os.environ)
    print(os.environ['name'])

    event = {}
    event['queryStringParameters'] = {}
    event['queryStringParameters']['name'] = os.environ['name']
    lambda_handler(event, None)
    