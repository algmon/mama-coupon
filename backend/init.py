import sqlite3
import hashlib
import datetime
import secrets

def connect_and_create_tables(db_path: str):
    """
    Connects to a SQLite database and creates the necessary tables.

    Args:
        db_path: The path to the SQLite database file.
    """

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            token TEXT,
            last_active DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()

def connect_and_drop_tables(db_path: str):
    """
    Connects to a SQLite database and drops all tables.

    Args:
        db_path: The path to the SQLite database file.
    """

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    # Drop all tables
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()

def connect_and_add_users(db_path: str, users: list):
    """
    Connects to a SQLite database and adds the provided users to the users table with improved security.

    Args:
        db_path: The path to the SQLite database file.
        users: A list of dictionaries, where each dictionary represents a user with the following keys:
            - username: The username of the user.
            - password: The password of the user.
    """

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    cursor = conn.cursor()

    try:
        # Hash passwords using SHA-256
        for user in users:
            username = user["username"]
            password = user["password"]

            # Hash the password using SHA-256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Generate a secure token
            token = secrets.token_urlsafe(32)

            # Store the datetime
            last_active = datetime.datetime.now()

            # Insert the user into the database
            cursor.execute("INSERT INTO users (username, password_hash, token, last_active) VALUES (?, ?, ?, ?)", (username, hashed_password, token, last_active))

        # Commit the transaction
        conn.commit()

    except sqlite3.Error as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        raise e

    finally:
        # Close the database connection
        conn.close()

def connect_and_clear_users(db_path: str):
    """
    Connects to a SQLite database and clears all users from the users table.

    Args:
        db_path: The path to the SQLite database file.
    """

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Delete all users from the users table
    cursor.execute("DELETE FROM users")

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()

def connect_and_list_users(db_path: str):
    """
    Connects to a SQLite database and lists all users in the users table.

    Args:
        db_path: The path to the SQLite database file.
    """

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to get all users
    cursor.execute("SELECT * FROM users")

    # Fetch all results
    users = cursor.fetchall()

    # Print the users
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}, Token: {user[3]}, Last Active: {user[4]}")

    # Close the database connection
    conn.close()

# Specify the path to your SQLite database file
db_path = "users.db"

# Create a list of users to add
users = [
    {"username": "user1", "password": "password123"},
    {"username": "user2", "password": "password456"},
    {"username": "user3", "password": "password789"},
]

#TODO fix connect_and_clear_users(db_path)
#TODO fix connect_and_drop_tables(db_path)

connect_and_create_tables(db_path)
connect_and_add_users(db_path, users)

connect_and_list_users(db_path)