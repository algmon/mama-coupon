from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
# Import your user management module here

import user_management

from aiChat import api_aiChat

class User(BaseModel):
    username: str
    email: str
    password: str
    phone: str

app = FastAPI()
app.include_router(api_aiChat, prefix="/aiChat", tags=["linkai聊天接口"])
#配置允许域名
origins = [
    "http://localhost:9527"
]
# 配置允许域名列表、允许方法、请求头、cookie等
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the 算法妈妈 User Management Module with Improved Security"}

@app.get("/active_users")
async def get_active_users(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """
    Returns the number of active users within a specified date range.

    Args:
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.

    Returns:
        A JSON response with the number of active users.
    """

    # Get active users from your user management module
    #active_users = user_management.get_active_users(start_date, end_date)
    active_users = user_management.get_active_users_from_db("users.db", start_date, end_date)

    return {"active_users": len(active_users)}

@app.post("/login")
async def login_user(
        request : Request
):
    """
    Logs in a user on the platform.

    Args:
        username: The username of the user.
        password: The password of the user.

    Returns:
        A JSON response with the status of the login.
    """

    # Authenticate the user in your user management module
    json_data = await request.json()

    username = json_data.get('username')
    password = json_data.get('password')
    success, token = user_management.login_user_to_db("users.db", username, password)

    if success:
        return {"message": "Login successful.", "code": 20000,"data": {
            "token": token
        }}
    else:
        return {"message": "Login failed."}, 401

@app.post("/register")
async def register_user(
    request: Request
):
    """
    Registers a new user on the platform.

    Args:
        username: The username of the new user.
        password: The password of the new user.

    Returns:
        A JSON response with the status of the registration.
    """

    # Register the user in your user management module
    data = await request.json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    success = user_management.register_user_to_db("users.db", username, password,email,phone)

    if success:
        return {"message": "Login successful.", "code": 20000}
    else:
        return {"message": "Registration failed."}, 400

@app.get("/total_users")
async def get_total_users():
    """
    Returns the total number of users on the platform.

    Returns:
        A JSON response with the total number of users.
    """

    # Get total users from your user management module
    total_users = user_management.get_total_users_from_db("users.db")


    return {"total_users": total_users}

@app.get("/users")
async def get_users():
    """
    Returns a list of all users on the platform.

    Returns:
        A JSON response with a list of users.
    """

    # Get all users from your user management module
    users = user_management.get_users_from_db("users.db")

    return {"users": users}

@app.get("/user/info")
async def useInfo(reqest : Request):
    data = {
        "code": 20000,
        "data": {
            "roles": ["admin"],
            "introduction": "I am a super administrator",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": "Super Admin"
        }
    }
    return {"data": data}