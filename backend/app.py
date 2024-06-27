from fastapi import FastAPI, Depends
from typing import Optional
from pydantic import BaseModel

#Import your user management module here
import user_management

class User(BaseModel):
    username: str
    email: str
    password: str

app = FastAPI()

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
    username: str,
    password: str,
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
    success, token = user_management.login_user_to_db("users.db", username, password)


    if success:
        return {"message": "Login successful.", "token": token}
    else:
        return {"message": "Login failed."}, 401

@app.post("/register")
async def register_user(
    username: str,
    password: str,
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
    success = user_management.register_user_to_db("users.db", username, password)

    if success:
        return {"message": "User registered successfully."}
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