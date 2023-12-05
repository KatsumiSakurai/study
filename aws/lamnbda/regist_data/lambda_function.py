import pandas as pd
from sqlalchemy import create_engine

connection_config = {
    'user': 'postgres',
    'password': 'TearBirds0',
    'host': 'sakurai-database-1.cneg46zalaof.ap-northeast-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'aichi'
}

def lambda_handler(event, context):
    fname = '346085_1413466_misc.csv'

    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))


    df = pd.read_csv(fname, encoding='utf8')
    print(df)
    df.to_sql('population', engine)


if __name__ == '__main__':
    lambda_handler(None, None)