import psycopg2
import json
from decimal import Decimal

connection_config = {
    'user': 'postgres',
    'password': 'refrain0',
    'host': 'test-database-1.cluster-c8ml75azbqsk.ap-northeast-1.rds.amazonaws.com',
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

    rows = []
    with psycopg2.connect(**connection_config) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT "地域名","市区町村名","総人口","男","女" FROM population WHERE "地域名"=' + "'" + name + "'")
            rows = cur.fetchall()

    data = [{'地域名': x[0], '市区町村名': x[1], '総人口': x[2], '男性人口': x[3], '女性人口': x[4]} for x in rows]

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(data, default=decimal_default_proc)
    }