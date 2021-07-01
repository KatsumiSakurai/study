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

def lambda_handler(event, context):
    with psycopg2.connect(**connection_config) as conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE progress ("地域名","status")')
            rows = cur.fetchall()