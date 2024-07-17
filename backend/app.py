import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import user_management
import advertiser_management
import ad_management
import recommendation_management


from aiChat import api_aiChat
from common.db import get_db_connection
from common.exception import exception
from common.resp import SuccessResponseData, ErrorResponseData
from fashion_video import api_fashion_video
from mysql.connector import cursor, connect
from fastapi import Request, HTTPException, Response
from typing import Optional

from common.interceptor import Interceptor

from datetime import datetime
import schedule
import time


class User(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    id: str
    token: str


class Ad(BaseModel):
    adname: str
    creator: str
    object_url: str

class UserRegistration(BaseModel):
    username: str
    last_updated_at: str
    is_active: str
    avatar_url: str
    fashion_score: int
    fashion_eval_reason: str


app = FastAPI()
# 应用中间件
# 定义中间件类


app.include_router(api_aiChat, prefix="/aiChat", tags=["linkai聊天接口"])
app.include_router(api_fashion_video, prefix="/fashionVideo", tags=["时尚接口"])
# 注册中间件


# def auth_middleware(request: Request, call_next):
#     # 从请求头中获取 token
#     print(request.headers.get("token"))
#     token = request.headers.get("token")
#     if not token:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     response = call_next(request)
#     return response


# 配置允许域名
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

# 在应用程序状态中存储数据库连接
app.state.db = None
# 应用程序启动和关闭事件


@app.on_event("startup")
async def startup_event():
    # 使用 app.state 来存储数据库连接
    app.state.db = get_db_connection()


@app.on_event("shutdown")
async def shutdown_event():
    # 检查数据库连接是否存在，并且关闭它
    db = app.state.db
    if db and not db.is_connected():
        db.close()

# 依赖项，用于获取全局数据库连接的游标


def get_db_cursor():
    if app.state.db is None:
        exception(500, "Database connection is not initialized")
    return app.state.db.cursor()


# 添加中间件到应用
app.add_middleware(Interceptor)


@app.get("/")
async def root():
    print("root() is called.")
    return {"message": "Welcome! You reach the Suanfamama AIGC Cognitive Computational Advertising Platform Backend."}


# # User Management
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
    # active_users = user_management.get_active_users(start_date, end_date)
    active_users = user_management.get_active_users_from_db(
        "./db/users.db", start_date, end_date, get_db_cursor())

    return {"active_users": len(active_users)}


@app.post("/users/login")
async def login_user(request: Request):
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
    success, user = user_management.login_user_to_db(
        "./db/users.db", username, password, app.state.db.cursor())

    if success:
        return {"message": "User Login successful.", "code": 200, "data": {
            "token": user[3],
            "userInfo": user
        }}
    else:
        return ErrorResponseData(501, "User Login failed.")
    #    return SuccessResponseData(data={"advInfo": advInfos},msg='获取成功')


@app.post("/users/register")
async def register_user(request: Request, db: cursor.MySQLCursor = Depends(get_db_cursor)):
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
    success = user_management.register_user_to_db(
        "./db/users.db", username, password, email, phone, app.state.db.cursor())

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
    total_users = user_management.get_total_users_from_db(
        "./db/users.db", get_db_cursor())
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
    user = user_management.get_spcific_user_from_db(
        "./db/users.db", int(user_id), get_db_cursor())
    if user:
        return {"user": user}
    else:
        return {"message": "User not found."}, 404


@app.get("/user/info")
async def useInfo(reqest: Request):
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
    active_ads = ad_management.get_active_ads_from_db(
        "./db/ads.db", get_db_cursor())
    return {"active_ads": active_ads}


@app.get("/ads/total_ads")
async def get_total_ads():
    """
    Returns the total number of ads on the platform.

    Returns:
        A JSON response with the total number of ads.
    """
    total_ads = ad_management.get_total_ads_from_db(
        "./db/ads.db", get_db_cursor())
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
    ad = ad_management.get_spcific_ad_from_db(
        "./db/ads.db", int(ad_id), get_db_cursor())
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
    success = ad_management.update_ad("./db/ads.db", ad_data, get_db_cursor())

    if success:
        return {"message": "Ad updated successfully.", "code": 200}
    else:
        return {"message": "Ad update failed."}, 400

# Advertiser Management


@app.get("/advertisers/active_advertisers")
async def get_active_advertisers(start_date: Optional[str] = None, end_date: Optional[str] = None,):
    """
    TODO: Returns the number of active advertisers within a specified date range.

    Args:
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.

    Returns:
        A JSON response with the number of active advertisers.
    """
    pass


@app.post("/advertisers/create")
async def create(request: Request):
    """
    Creates an ad on the platform.

    Args:
        prompt:
        negative_prompt:

    Returns:
        A JSON response with the status of the creation.
    """
    try:
        # Get data from the request body
        json_data = await request.json()
        prompt = json_data.get('prompt')
        negative_prompt = json_data.get('negative_prompt')

        # prompt = "a dog"
        # negative_prompt = "hands and face"

        # Create an ad image
        success = advertiser_management.create_an_ad(
            prompt, negative_prompt, get_db_cursor())

        if success:
            return JSONResponse(
                status_code=200,
                content={"message": "Ad image created successfully.",
                         "code": 200, "data": {}}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"message": "Ad image creation failed."}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error creating ad image: {e}"}
        )

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
    total_ads = ad_management.get_total_ads_from_db(
        "./db/ads.db", get_db_cursor())
    num_ads_recommend = 11  # TODO: ADD to global config
    matches = recommendation_management.match_for_specific_user(
        user_id, total_ads, num_ads_recommend)
    return {"matches": matches}


@app.get("/advertisers/getAdv")
async def getAdv(request: Request):
    print(request.headers.get("token"))
    userId = user_management.get_user_id_by_token(
        "./db/users.db", request.headers.get("token"), get_db_cursor())
    advInfos = []
    total_ads = ad_management.get_total_ads_from_db(
        "./db/ads.db", get_db_cursor())
    num_ads_recommend = 11  # TODO: ADD to global config
    ads = recommendation_management.match_for_specific_user(
        userId, total_ads, num_ads_recommend)
    # 访问 'matches' 列表
    matched_ads_list = (ads[0].get('matched_ads', []))
    # 现在 matched_ads_list 包含了您需要的列表
    print("matched_ads_list:", matched_ads_list)
    for adv in matched_ads_list:
        advInfo = ad_management.get_spcific_ad_from_db(
            "./db/ads.db", int(adv), get_db_cursor())
        advInfos.append(advInfo)
    print("advInfos:", advInfos)
    return SuccessResponseData(data={"advInfo": advInfos}, msg='获取成功')



#注册相机拍摄的用户
def register_user_by_camera(username,avatar_url,fashion_score,fashion_eval_reason):

    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    last_updated_at = formatted_now
    is_active = "1"
    success = user_management.register_user_by_camera_to_db(
        "./db/users.db", username, last_updated_at, is_active, avatar_url, fashion_score, fashion_eval_reason,  app.state.db.cursor())

    if success:
        return {"message": "User Registration successful.", "code": 200}
    else:
        return {"message": "Registration failed."}, 400


#定时器 定时调用相机拍摄解析照片的相关方法
#TODO: #未填写具体的方法内容
schedule.every(10).seconds.do()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    schedule.run_pending()  # 运行所有可以运行的任务
    time.sleep(1)  # 等待一秒
