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

    # Create the 'advertisers' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advertisers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            advertisername TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def connect_and_drop_tables(db_path: str):
    """
    Connects to a SQLite database and drops all tables.

    Args:
        db_path: The path to the SQLite database file.
    """
    pass

def connect_and_add_advertisers(db_path: str, advertisers: list):
    """
    Connects to a SQLite database and adds the provided advertisers to the advertisers table with improved security.

    Args:
        db_path: The path to the SQLite database file.
        advertisers: A list of dictionaries, where each dictionary represents a advertiser with the following keys:
            - advertisername: The advertisername of the advertiser.
            - password: The password of the advertiser.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for advertiser in advertisers:
        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(advertiser["password"].encode()).hexdigest()

        # Insert the advertiser into the database
        try:
            cursor.execute(
                """
                INSERT INTO advertisers (advertisername, password)
                VALUES (?, ?)
                """,
                (advertiser["advertisername"], hashed_password),
            )
            conn.commit()
            print(f"Added advertiser: {advertiser['advertisername']}")
        except sqlite3.IntegrityError:
            print(
                f"Advertiser with name '{advertiser['advertisername']}' already exists."
            )

    conn.close()

def connect_and_clear_advertisers(db_path: str):
    """
    Connects to a SQLite database and clears all advertisers from the advertisers table.

    Args:
        db_path: The path to the SQLite database file.
    """
    pass

def connect_and_list_advertisers(db_path: str):
    """
    Connects to a SQLite database and lists all advertisers in the advertisers table.

    Args:
        db_path: The path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the query to retrieve all advertisers
    cursor.execute("SELECT * FROM advertisers")

    # Fetch all rows as a list of dictionaries
    advertisers = [
        dict(id=row[0], advertisername=row[1], password=row[2], created_at=row[3])
        for row in cursor.fetchall()
    ]

    # Print the list of advertisers
    for advertiser in advertisers:
        print(f"ID: {advertiser['id']}, Advertiser Name: {advertiser['advertisername']}, Created At: {advertiser['created_at']}")

    # Close the database connection
    conn.close()

# Specify the path to your SQLite database file
db_path = "./db/advertisers.db"

# Create a list of gen advertisers at scale
advertisers = []
NUM_ADVERTISERS_GEN = 999999

for i in range(NUM_ADVERTISERS_GEN):
    advertiser = {
        "advertisername": f"advertiser_{i+1}",
        "password": f"password{i+1}"
    }
    advertisers.append(advertiser)

'''
# Create a list of typical advertisers
advertisers = [
    {"advertisername": "Suanfamama", "password": "withmama"},
    {"advertisername": "Google", "password": "withmama"},
    {"advertisername": "Microsoft", "password": "withmama"},
]
'''

#connect_and_clear_advertisers(db_path)
#connect_and_create_tables(db_path)
connect_and_add_advertisers(db_path, advertisers)
connect_and_list_advertisers(db_path)