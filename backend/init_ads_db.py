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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the 'ads' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adname TEXT NOT NULL,
            creator TEXT NOT NULL,
            "object-url" TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def connect_and_drop_tables(db_path: str):
    """
    Connects to a SQLite database and drops all tables.

    Args:
        db_path: The path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop the 'ads' table
    cursor.execute("DROP TABLE IF EXISTS ads")

    conn.commit()
    conn.close()

def connect_and_add_ads(db_path: str, ads: list):
    """
    Connects to a SQLite database and adds the provided ads to the ads table with improved security.

    Args:
        db_path: The path to the SQLite database file.
        ads: A list of dictionaries, where each dictionary represents an ad with the following keys:
            - adname: The adname of the ad.
            - creator: The creator of the ad.
            - object-url: The object url of the ad.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for ad in ads:
        # Prepare the SQL statement
        sql = """
            INSERT INTO ads (adname, creator, "object-url")
            VALUES (?, ?, ?)
        """

        # Execute the SQL statement with the ad data
        cursor.execute(sql, (ad['adname'], ad['creator'], ad['object-url']))

    conn.commit()
    conn.close()

def connect_and_clear_ads(db_path: str):
    """
    Connects to a SQLite database and clears all ads from the ads table.

    Args:
        db_path: The path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Delete all rows from the 'ads' table
    cursor.execute("DELETE FROM ads")

    conn.commit()
    conn.close()

def connect_and_list_ads(db_path: str):
    """
    Connects to a SQLite database and lists all ads in the ads table.

    Args:
        db_path: The path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all ads from the 'ads' table
    cursor.execute("SELECT * FROM ads")
    ads = cursor.fetchall()

    # Print the ads
    for ad in ads:
        print(f"ID: {ad[0]}, Ad Name: {ad[1]}, Creator: {ad[2]}, Object URL: {ad[3]}, Created At: {ad[4]}")

    conn.close()

# Specify the path to your SQLite database file
db_path = "ads.db"

# Create a list of ads to add
ads = [
    {"adname": "ad1", "creator": "creator a", "object-url": ""},
    {"adname": "ad2", "creator": "creator b", "object-url": ""},
    {"adname": "ad3", "creator": "creator c", "object-url": ""},
]

connect_and_create_tables(db_path)
connect_and_add_ads(db_path, ads)
connect_and_list_ads(db_path)