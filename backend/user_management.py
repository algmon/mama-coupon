import datetime
import secrets
import sqlite3
import hashlib

from common.exception import exception


def get_active_users_from_db(db_path: str, start_date: str = None, end_date: str = None, db: object=None):
    """
    Gets a list of active users from a SQLite database within a specified date range.

    Args:
        db_path: The path to the SQLite database file.
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.

    Returns:
        A list of active users, where each user is a dictionary with the following keys:
        - id: The user's ID.
        - username: The user's username.
        - last_active: The user's last active date and time.
    """

    # Connect to the database
    # conn = sqlite3.connect(db_path)

    # Create a cursor object
    # cursor = conn.cursor()

    # Execute the query to get active users
    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        db.execute(
            "SELECT id, username, last_active FROM users WHERE last_active >= %s AND last_active <= %s",
            (start_date, end_date),
        )
    else:
        db.execute("SELECT id, username, last_active FROM users")

    # Fetch all rows as a list of dictionaries
    active_users = [
        dict(id=row[0], username=row[1], last_active=row[2]) for row in db.fetchall()
    ]

    # Close the database connection
    # conn.close()

    return active_users

def get_total_users_from_db(db_path: str,db: object):
    """
    Gets the total number of users from a SQLite database.

    Args:
        db_path: The path to the SQLite database file.

    Returns:
        An integer representing the total number of users.
    """

    # Connect to the database
    # conn = sqlite3.connect(db_path)

    # Create a cursor object
    # cursor = conn.cursor()

    # Execute the query to get the total number of users
    db.execute("SELECT COUNT(*) FROM users")

    # Fetch the result
    total_users = db.fetchone()[0]

    # Close the database connection
    # conn.close()

    return total_users

def get_users_from_db(db_path: str, db: object):
    """
    Gets a list of users from a SQLite database.

    Args:
        db_path: The path to the SQLite database file.

    Returns:
        A list of users, where each user is a dictionary with the following keys:
        - id: The user's ID.
        - username: The user's username.
        - password: The user's password (hashed).
        - last_active: The user's last active date and time.
    """

    # Connect to the database
    # conn = sqlite3.connect(db_path)

    # Create a cursor object
    # cursor = conn.cursor()

    # Execute the query to get all users
    db.execute("SELECT * FROM users")

    # Fetch all rows as a list of dictionaries
    users = [
        dict(id=row[0], username=row[1], password=row[2], token=row[3], last_active=row[4])
        for row in db.fetchall()
    ]

    # Close the database connection
    # conn.close()

    return users

def register_user_to_db(db_path: str,
                        username: str,
                        password: str,
                        email: str,
                        phone: str,
                        db: object):
    """
    Registers a new user to the database with improved security..

    Args:
        db_path: The path to the SQLite database file.
        username: The username of the new user.
        password: The password of the new user.
        email: The email of the new user.
        phone: The phone of the new user.

    Returns:
        True if the registration is successful, False otherwise.
    """

    # # Connect to the database
    # conn = sqlite3.connect(db_path)
    #
    # # Create a cursor object
    # cursor = conn.cursor()
    #
    # # Create the users table if it doesn't exist
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS users (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         username TEXT UNIQUE NOT NULL,
    #         password TEXT NOT NULL,
    #         email TEXT ,
    #         phone TEXT ,
    #         last_active DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    #     )
    # """)
    #
    # # Check if the username already exists
    # cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    # user = cursor.fetchone()
    # cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    # userPhone = cursor.fetchone()
    # if user or userPhone:
    #  # Username already exists
    #   exception(501 , "Username or phone already exists")
    #
    # # Hash the password using SHA-256
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
    #
    # # Generate a secure token
    # token = secrets.token_urlsafe(32)
    #
    # # Insert the new user into the database
    # cursor.execute("INSERT INTO users (username, password_hash, token,email,phone) VALUES (?, ?, ?,?,?)", (username, hashed_password, token,email,phone))
    #
    # # Commit the changes
    # conn.commit()
    #
    # # Close the database connection
    # conn.close()
    # db = await get_db()
# 检查用户名是否已存在
    db.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = db.fetchone()
    db.execute("SELECT * FROM users WHERE phone = %s", (phone,))
    userPhone = db.fetchone()
    if user or userPhone:
        # 用户名或手机号已存在
        exception(501 , "Username or phone already exists")

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print(hashed_password)
    # Generate a secure token
    token = secrets.token_urlsafe(32)

    # 插入新用户到数据库
    db.execute("""
        INSERT INTO users (username, password_hash, token, email, phone) 
        VALUES (%s, %s, %s, %s, %s)
    """, (username, hashed_password, token,email,phone))

    # 提交更改
    # db.connection.commit()
    # db.execute("COMMIT")
    return True



def login_user_to_db(db_path: str, username: str, password: str , db: object):
    """
    Logs in a user on the platform using the database.

    Args:
        username: The username of the user.
        password: The password of the user.

    Returns:
        A tuple containing a boolean indicating success and a token if successful, otherwise None.
    """

    # Connect to the database
    # conn = sqlite3.connect(db_path)

    # Create a cursor object
    # cursor = conn.cursor()

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Execute the query to get the user with the matching username and password
    db.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, hashed_password))

    # Fetch the user data
    user = db.fetchone()

    # Close the database connection
    # db.close()

    # Check if the user was found
    if user:
        # TODO: Get the token from db with improved security
        userInfo = user
        return True, userInfo
    else:
        return False, None
    
def get_spcific_user_from_db(db_path: str, user_id: int, db: object):
    """
    Gets a specific user from a SQLite database based on its ID.

    Args:
        db_path: The path to the SQLite database file.
        user_id: The ID of the user to retrieve.

    Returns:
        A dictionary representing the user, or None if the user is not found.
    """
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()

    # Execute the query to get the specific user
    db.execute("SELECT * FROM users WHERE id = %s", (user_id,))

    # Fetch the result
    row = db.fetchone()

    # Close the database connection
    # conn.close()

    if row:
        # Convert the row to a dictionary
        user = dict(id=row[0], username=row[1], password=row[2], token=row[3], last_active=row[4])
        return user
    else:
        return None

def get_user_id_by_token(db_path: str, token: str, db: object):
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()

    # Execute the query to get the specific user
    db.execute("SELECT id FROM users WHERE token = %s", (token,))

    # Fetch the result
    userId = db.fetchone()

    # Close the database connection
    # conn.close()
    return userId

