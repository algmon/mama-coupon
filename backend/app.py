from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

import user_management
import ad_management
import recommendation_management

from aiChat import api_aiChat

class User(BaseModel):
    username: str
    email: str
    password: str
    phone: str

class Ad(BaseModel):
    adname: str
    creator: str
    object_url: str

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
    return {"message": "Welcome! You reach the Suanfamama Cognitive Computational Advertising Platform Backend with Improved Stability and Security."}


# User Management
@app.get("/users/active_users")
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
    active_users = user_management.get_active_users_from_db("./db/users.db", start_date, end_date)

    return {"active_users": len(active_users)}

@app.post("/users/login")
async def login_user(request : Request):
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
    success, token = user_management.login_user_to_db("./db/users.db", username, password)

    if success:
        return {"message": "User Login successful.", "code": 200,"data": {
            "token": token
        }}
    else:
        return {"message": "User Login failed."}, 401

@app.post("/users/register")
async def register_user(request: Request):
    """
    Registers a new user on the platform.

    Args:
        username: The username of the new user.
        email: The email of the new user.
        password: The password of the new user.
        phone: The phone number of the new user.

    Returns:
        A JSON response with the status of the registration.
    """

    data = await request.json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    success = user_management.register_user_to_db("./db/users.db", username, password,email,phone)

    if success:
        return {"message": "User Registration successful.", "code": 200}
    else:
        return {"message": "Registration failed."}, 400

@app.get("/users/total_users")
async def get_total_users():
    """
    Returns the total number of users on the platform.

    Returns:
        A JSON response with the total number of users.
    """
    # Get total users from your user management module
    total_users = user_management.get_total_users_from_db("./db/users.db")
    return {"total_users": total_users}

@app.get("/users/{user_id}")
async def get_specific_user(user_id: str):
    """
    Returns a specific user on the platform.

    Args:
        user_id: The ID of the user.

    Returns:
        A JSON response with the user details.
    """
    user = user_management.get_spcific_user_from_db("./db/users.db", int(user_id))
    if user:
        return {"user": user}
    else:
        return {"message": "User not found."}, 404

@app.get("/user/info")
async def useInfo(reqest : Request):
    data = {
        "code": 200,
        "data": {
            "roles": ["admin"],
            "introduction": "I am a super administrator",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": "Super Admin"
        }
    }
    return {"data": data}

# Ad Management
@app.get("/ads/active_ads")
async def get_active_ads():
    """
    TODO: Returns a list of active ads on the platform.

    An ad is considered active if its 'object-url' field is not empty.

    Returns:
        A JSON response with a list of active ads.
    """
    active_ads = ad_management.get_active_ads_from_db("./db/ads.db")
    return {"active_ads": active_ads}

@app.get("/ads/total_ads")
async def get_total_ads():
    """
    Returns the total number of ads on the platform.

    Returns:
        A JSON response with the total number of ads.
    """
    total_ads = ad_management.get_total_ads_from_db("./db/ads.db")
    return {"total_ads": total_ads}

@app.get("/ads/{ad_id}")
async def get_specific_ad(ad_id: str):
    """
    Returns a specific ad on the platform.

    Args:
        ad_id: The ID of the ad.

    Returns:
        A JSON response with the ad details.
    """
    ad = ad_management.get_spcific_ad_from_db("./db/ads.db", int(ad_id))
    if ad:
        return {"ad": ad}
    else:
        return {"message": "Ad not found."}, 404

@app.post("/ads/update")
async def update_specific_ad(request: Request):
    """
    Updates a specific ad on the platform.

    Args:
        ad_id:
        adname:
        creator:
        object_url:

    Returns:
        A JSON response with the status of the update.
    """
    # Get the updated ad data from the request body
    json_data = await request.json()

    ad_id = json_data.get('ad_id')
    adname = json_data.get('adname')
    creator = json_data.get('creator')
    object_url = json_data.get('object_url')
    
    ad_data = {
        "adname": adname,
        "creator": creator,
        "object_url": object_url,
        "ad_id": ad_id
    }

    # Update the ad in your ad management module
    success = ad_management.update_ad("./db/ads.db", ad_data)

    if success:
        return {"message": "Ad updated successfully.", "code": 200}
    else:
        return {"message": "Ad update failed."}, 400

# Advertiser Management
@app.get("/advertisers/active_advertisers")
async def get_active_advertisers(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """
    Returns the number of active advertisers within a specified date range.

    Args:
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.

    Returns:
        A JSON response with the number of active advertisers.
    """
    pass

# Recommendation Management
@app.get("/match/{user_id}")
async def get_matches_for_specifc_user(user_id):
    """
    Returns a list of matches for a specific user at specific time on the platform.

    Args:
        user_id: The ID of the user.

    Returns:
        A JSON response with a list of ads.
    """
    total_ads = ad_management.get_total_ads_from_db("./db/ads.db")
    num_ads_recommend = 11 # TODO: ADD to global config
    matches = recommendation_management.match_for_specific_user(user_id, total_ads, num_ads_recommend)
    return {"matches": matches}