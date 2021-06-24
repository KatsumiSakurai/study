import psycopg2
import json
from decimal import Decimal

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

    rows = []
    with psycopg2.connect(**connection_config) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT "地域コード","都道府県名","地域名",sum("総人口"),sum("男"),sum("女") FROM population GROUP BY "地域コード","都道府県名","地域名"')
            rows = cur.fetchall()

    data = [{'地域コード': x[0], '都道府県名': x[1], '地域名': x[2], '総人口': x[3], '男性人口': x[4], '女性人口': x[5]} for x in rows if x[0] not in [0, 10]]
    data = sorted(data, key=lambda x:x['地域コード'])

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(data, default=decimal_default_proc)
    }