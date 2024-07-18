# 针对相机拍摄的图片进行自动注册用户
import secrets
from logging import exception


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