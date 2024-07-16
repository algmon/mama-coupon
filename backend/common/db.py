from fastapi import Depends
from mysql.connector import connect
import json


def read_config_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def get_db_connection():
    config = read_config_file('config.json')
    db_config = config['database']
    connection = connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
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
