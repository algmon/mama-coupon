from fastapi import Depends
from mysql.connector import connect

def get_db_connection():
    connection = connect(
        host='106.53.173.82',
        user="suanfamama",
        password="suanfamama123",
        database="platform-common"
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