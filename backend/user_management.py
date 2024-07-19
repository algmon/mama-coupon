import datetime
import secrets
import sqlite3
import hashlib

from common.exception import exception


def get_active_users_from_db(db_path: str, start_date: str = None, end_date: str = None, db: object = None):
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


def get_total_users_from_db(db_path: str, db: object):
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
        dict(id=row[0], username=row[1], password=row[2],
             token=row[3], last_active=row[4])
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
        exception(501, "Username or phone already exists")

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print(hashed_password)
    # Generate a secure token
    token = secrets.token_urlsafe(32)

    # 插入新用户到数据库
    db.execute("""
        INSERT INTO users (username, password_hash, token, email, phone) 
        VALUES (%s, %s, %s, %s, %s)
    """, (username, hashed_password, token, email, phone))

    # 提交更改
    # db.connection.commit()
    # db.execute("COMMIT")
    return True


def login_user_to_db(db_path: str, username: str, password: str, db: object):
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
    print("Login(...) is called.")
    print("username:" + username)
    print("hashed_password:" + hashed_password)
    print()
    # Execute the query to get the user with the matching username and password
    db.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s",
               (username, hashed_password))
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
        user = dict(id=row[0], username=row[1],
                    password=row[2], token=row[3], last_active=row[4])
        return user
    else:
        return None


def get_user_id_by_token(db_path: str, token: str, db: object):

    # Execute the query to get the specific user
    db.execute("SELECT id FROM users WHERE token = %s", (token,))

    # Fetch the result
    userId = db.fetchone()

    # Close the database connection
    # conn.close()
    return userId


def get_user_by_developer_token(mama_api_key: str, db: object):
    db.execute("SELECT * FROM developers WHERE mama_api_key = %s",
               (mama_api_key,))
    # Fetch the result
    userInfo = db.fetchone()

    return userInfo


def like_ads_to_db(user_id: str, ads_id: str, db: object):
    db.execute("""SELECT * FROM user_ads WHERE user_id = %s""", (user_id,))
    fetchone = db.fetchone()
    if fetchone:
        db.execute("""SELECT user_like FROM user_ads WHERE user_id = %s""", (user_id,))
        db_fetchone = db.fetchone()
        if db_fetchone[0] is not None:
            s = list(db_fetchone)
            if isinstance(s[0], str):
                # 尝试将字符串转换为列表
                try:
                    s[0] = eval(s[0])
                except Exception as e:
                    print(f"将字符串转换为列表时出错: {e}")
                    return None
            if isinstance(s[0], list):
                # 检查列表中是否包含传入的 ads_id
                if int(ads_id) in s[0]:
                    s[0].remove(int(ads_id))
                    db.execute("""SELECT `like` FROM ads WHERE id = %s""", (ads_id,))
                    likeNum = db.fetchone()[0]  # 获取 like 字段的值
                    db.execute("""UPDATE ads SET `like` = %s WHERE id = %s""", (likeNum - 1, ads_id))
                else:
                    s[0].append(int(ads_id))
                    db.execute("""SELECT `like` FROM ads WHERE id = %s""", (ads_id,))
                    likeNum = db.fetchone()[0]  # 获取 like 字段的值
                    db.execute("""UPDATE ads SET `like` = %s WHERE id = %s""", (likeNum + 1, ads_id))
                    db.execute("""select user_like from user_ads where user_id = %s""", (user_id,))
                    db.fetchone()
                updated_ads_id = str(s[0])
                sql = """UPDATE user_ads SET user_like = %s WHERE user_id = %s"""
                db.execute(sql, (updated_ads_id, user_id))
                return updated_ads_id
            else:
                print("s[0] 不是列表")
        else:
            ads_id_list = "[" + str(ads_id) + "]"
            sql = """UPDATE user_ads SET user_like = %s WHERE user_id = %s"""
            db.execute(sql, (ads_id_list, user_id))
            db.execute("""SELECT dislike FROM ads WHERE id = %s""", (ads_id,))
            fetch_dislike = db.fetchone()
            if fetch_dislike:
                likeNum = fetch_dislike[0]  # 获取 like 字段的值
                db.execute("""UPDATE ads SET `like` = %s WHERE id = %s""", (likeNum + 1, ads_id))
            else:
                print(f"广告 ID {ads_id} 不存在")
            return ads_id_list
        return None
    else:
        ads_id_list = "[" + str(ads_id) + "]"
        sql = """INSERT INTO user_ads (user_id, user_like) VALUES (%s, %s)"""
        db.execute(sql, (user_id, ads_id_list))
        db.execute("""SELECT `like` FROM ads WHERE id = %s""", (ads_id,))
        likeNum = db.fetchone()[0]  # 获取 like 字段的值
        db.execute("""UPDATE ads SET `like` = %s WHERE id = %s""", (likeNum + 1, ads_id))
        return ads_id_list




def dislike_ads_to_db(user_id: str, ads_id: str, db: object):
    db.execute("""SELECT * FROM user_ads WHERE user_id = %s""", (user_id,))
    fetchone1 = db.fetchone()
    if fetchone1:
        db.execute("""SELECT user_dislike FROM user_ads WHERE user_id = %s""", (user_id,))
        fetchone = db.fetchone()
        if fetchone[0] is not None:
            db.execute("""SELECT user_dislike FROM user_ads WHERE user_id = %s""", (user_id,))
            db_fetchone = db.fetchone()
            if db_fetchone:
                s = list(db_fetchone)
                if isinstance(s[0], str):
                    # 尝试将字符串转换为列表
                    try:
                        s[0] = eval(s[0])
                    except Exception as e:
                        print(f"将字符串转换为列表时出错: {e}")
                        return None
                if isinstance(s[0], list):
                    # 检查列表中是否包含传入的 ads_id
                    if int(ads_id) in s[0]:
                        s[0].remove(int(ads_id))
                        db.execute("""SELECT dislike FROM ads WHERE id = %s""", (ads_id,))
                        fetch_dislike = db.fetchone()
                        if fetch_dislike:
                            dislikeNum = fetch_dislike[0]  # 获取 dislike 字段的值
                            db.execute("""UPDATE ads SET dislike = %s WHERE id = %s""", (dislikeNum - 1, ads_id))
                        else:
                            print(f"广告 ID {ads_id} 不存在")
                    else:
                        s[0].append(int(ads_id))
                        db.execute("""SELECT dislike FROM ads WHERE id = %s""", (ads_id,))
                        fetch_dislike = db.fetchone()
                        if fetch_dislike:
                            dislikeNum = fetch_dislike[0]  # 获取 dislike 字段的值
                            db.execute("""UPDATE ads SET dislike = %s WHERE id = %s""", (dislikeNum + 1, ads_id))
                        else:
                            print(f"广告 ID {ads_id} 不存在")
                    updated_ads_id = str(s[0])
                    sql = """UPDATE user_ads SET user_dislike = %s WHERE user_id = %s"""
                    db.execute(sql, (updated_ads_id, user_id))
                    return updated_ads_id
                else:
                    print("s[0] 不是列表")
            return None
        else:
            ads_id_list = "[" + str(ads_id) + "]"
            sql = """UPDATE user_ads SET user_dislike = %s WHERE user_id = %s"""
            db.execute(sql, (ads_id_list, user_id))
            db.execute("""SELECT dislike FROM ads WHERE id = %s""", (ads_id,))
            fetch_dislike = db.fetchone()
            if fetch_dislike:
                dislikeNum = fetch_dislike[0]  # 获取 dislike 字段的值
                db.execute("""UPDATE ads SET dislike = %s WHERE id = %s""", (dislikeNum + 1, ads_id))
            else:
                print(f"广告 ID {ads_id} 不存在")
            return ads_id_list
        return None
    else:
        ads_id_list = "[" + str(ads_id) + "]"
        sql = """INSERT INTO user_ads (user_id, user_dislike) VALUES (%s, %s)"""
        db.execute(sql, (user_id, ads_id_list))
        db.execute("""SELECT dislike FROM ads WHERE id = %s""", (ads_id,))
        fetch_dislike = db.fetchone()
        if fetch_dislike:
            dislikeNum = fetch_dislike[0]  # 获取 dislike 字段的值
            db.execute("""UPDATE ads SET dislike = %s WHERE id = %s""", (dislikeNum + 1, ads_id))
        else:
            print(f"广告 ID {ads_id} 不存在")
        return ads_id_list
    return None


def get_like_dislike_ads_from_db(user_id: str, db: object):
    db.execute("""select user_like, user_dislike from user_ads where user_id = %s""", (user_id,))
    fetchone = db.fetchone()
    if fetchone:
        return fetchone
    else:
        return None


def drag_and_drop_ads_to_db(user_id: str, ads_id_list: list, db: object):
    def fetch_user_drag_and_drop(user_id):
        db.execute("""select user_drag_and_drop from user_ads where user_id = %s""", (user_id,))
        fetchone = db.fetchone()
        if fetchone and fetchone[0] is not None:
            return fetchone[0]
        return None

    def update_user_drag_and_drop(user_id, updated_ads_id):
        sql = """UPDATE user_ads SET user_drag_and_drop = %s WHERE user_id = %s"""
        db.execute(sql, (updated_ads_id, user_id))

    def insert_user_drag_and_drop(user_id, ads_id_list):
        sql = """INSERT INTO user_ads (user_id, user_drag_and_drop) VALUES (%s, %s)"""
        db.execute(sql, (user_id, str(ads_id_list)))

    db.execute("""select * from user_ads where user_id = %s""", (user_id,))
    fetchone = db.fetchone()
    if fetchone:
        # 如果不是新用户
        user_drag_and_drop = fetch_user_drag_and_drop(user_id)
        if user_drag_and_drop:
            # 如果用户已经有拖拽的数据
            try:
                if isinstance(user_drag_and_drop, str):
                    user_drag_and_drop = eval(user_drag_and_drop)
                if isinstance(user_drag_and_drop, list):
                    for ads_id in ads_id_list:
                        if int(ads_id) not in user_drag_and_drop:
                            user_drag_and_drop.append(int(ads_id))
                    update_user_drag_and_drop(user_id, str(user_drag_and_drop))
                else:
                    raise ValueError("user_drag_and_drop 不是列表")
            except Exception as e:
                print(f"处理用户拖拽数据时出错: {e}")
                return False
        else:
            # 如果用户没有拖拽的数据, 则先插入拖拽的数据
            update_user_drag_and_drop(user_id, str(ads_id_list))
    else:
        # 如果是新用户, 就给添加以用户数据
        insert_user_drag_and_drop(user_id, ads_id_list)
    return True

# 针对相机拍摄的图片进行自动注册用户
def register_user_by_camera_to_db(db_path: str,
                        username: str,
                        last_updated_at: str,
                        is_active: str,
                        avatar_url: str,
                        fashion_score: int,
                        fashion_eval_reason: str,
                        db: object):
    # 检查用户名是否已存在
    db.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = db.fetchone()

    if user:
        # 用户名已存在
        exception(501, "Username already exists")

    # Generate a secure token
    token = secrets.token_urlsafe(32)

    # 插入新用户到数据库
    db.execute("""
            INSERT INTO users (username, last_updated_at, is_active, avatar_url, fashion_score, fashion_eval_reason) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, last_updated_at, is_active, avatar_url, fashion_score, fashion_eval_reason))


    return True

