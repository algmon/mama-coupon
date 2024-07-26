from fastapi import Depends
from mysql.connector import connect
import json
import os


def read_config_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def get_db_connection():
    '''
    # read config from local file
    config = read_config_file('config.json')
    db_config = config['database']
    connection = connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    '''
    connection = connect(
        host=os.environ['MAMA_DB_HOST'],
        user=os.environ['MAMA_DB_USER'],
        password=os.environ['MAMA_DB_PASSWORD'],
        database=os.environ['MAMA_DB_DATABASE']
    )
    # 开启自动提交模式
    connection.autocommit = True
    return connection


def get_db():
    connection = get_db_connection()
    db = connection.cursor()

    try:
        yield db
    finally:
        db.close()
        connection.close()
