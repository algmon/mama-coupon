import logging
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

# Configure the logging module
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to the console
        logging.FileHandler("app.log"),  # Log to a file
    ],
)

# 应用中间件
# 定义中间件类
app.include_router(api_aiChat, prefix="/aiChat", tags=["算法妈妈多模态能力接口"])
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

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = get_db_connection()
    response = await call_next(request)
    return response


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
    logging.info("Root endpoint accessed.")
    return {"message": "Welcome! You reach the Suanfamama AIGC Cognitive Computational Advertising Platform Backend."}

# User Management
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
    logging.info("login_user endpoint accessed.")

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

@app.post("/users/logout")
async def logout_user(request: Request, db: cursor.MySQLCursor = Depends(get_db_cursor)):
    """
    Logs out a user from the platform.

    Args:
        token: The user's authentication token.

    Returns:
        A JSON response indicating the success or failure of the logout.
    """
    logging.info("logout_user endpoint accessed.")
    # TODO: Needs Implementation
    pass

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
    logging.info("register_user endpoint accessed.")

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

@app.get("/users/{user_id}")
async def get_specific_user(user_id: str):
    """
    Returns a specific user on the platform.

    Args:
        user_id: The ID of the user.

    Returns:
        A JSON response with the user details.
    """
    logging.info(f"get_specific_user endpoint accessed with user_id: {user_id}")

    user = user_management.get_spcific_user_from_db(
        "./db/users.db", int(user_id), get_db_cursor())
    if user:
        return {"user": user}
    else:
        return {"message": "User not found."}, 404


@app.get("/user/info")
async def useInfo(reqest: Request):
    # TODO: discuss and decide whether to drop or NOT
    logging.info("useInfo endpoint accessed.")

    data = {
        "code": 200,
        "data": {
            "roles": ["user"],
            "introduction": "I am a user",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": "User Nobody"
        }
    }
    return {"data": data}

# Ad Management
@app.get("/ads/{ad_id}")
async def get_specific_ad(ad_id: str):
    """
    Returns a specific ad on the platform.

    Args:
        ad_id: The ID of the ad.

    Returns:
        A JSON response with the ad details.
    """
    logging.info(f"get_specific_ad endpoint accessed with ad_id: {ad_id}")

    ad = ad_management.get_spcific_ad_from_db(
        "./db/ads.db", int(ad_id), get_db_cursor())
    if ad:
        return {"ad": ad}
    else:
        return {"message": "Ad not found."}, 404

@app.post("/advertisers/update")
async def update_specific_ad(request: Request):
    """
    Updates a specific ad.

    Args:
        ad_id:
        adname:
        creator:
        object_url:

    Returns:
        A JSON response with the status of the update.
    """
    logging.info("update_specific_ad endpoint accessed. TODO: Needs Implementation.")

@app.post("/ads/update", deprecated=True)
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
    logging.info("update_specific_ad endpoint accessed.")

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
    logging.info("create endpoint accessed.")

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
    logging.info(f"get_matches_for_specifc_user endpoint accessed with user_id: {user_id}")

    total_ads = ad_management.get_total_ads_from_db(
        "./db/ads.db", get_db_cursor())
    num_ads_recommend = 11  # TODO: ADD to global config
    matches = recommendation_management.match_for_specific_user(
        user_id, total_ads, num_ads_recommend)
    return {"matches": matches}


@app.get("/advertisers/getAdv")
async def getAdv(request: Request):
    logging.info("getAdv endpoint accessed.")

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
    # matched_ads_list = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]   # 假设匹配到的广告列表
    # 现在 matched_ads_list 包含了您需要的列表
    print("matched_ads_list:", matched_ads_list)
    for adv in matched_ads_list:
        advInfo = ad_management.get_spcific_ad_from_db(
            "./db/ads.db", int(adv), get_db_cursor())
        advInfos.append(advInfo)
    print("advInfos:", advInfos)

    # 回显用户喜欢与不感兴趣的广告
    db = user_management.get_like_dislike_ads_from_db(userId[0], get_db_cursor())

    if (db != None):
        return SuccessResponseData(data={"advInfo": advInfos, "ads_list": matched_ads_list, "like": db[0], "dislike": db[1]}, msg='获取成功')
    else:
        return SuccessResponseData(data={"advInfo": advInfos, "ads_list": matched_ads_list}, msg='获取成功')


@app.post("/users/like")
async def like(request: Request):
    # 获取请求体中的数据
    request_body = await request.json()
    # 获取用户ID
    userId = user_management.get_user_id_by_token(
        "./db/users.db", request.headers.get("token"), get_db_cursor()
    )
    user_id = userId[0]
    # 广告ID
    ads_id = request_body.get("ads_id")

    db = user_management.like_ads_to_db(user_id, ads_id, get_db_cursor())
    # 返回响应
    return SuccessResponseData(data= db, msg='操作成功')


@app.post("/users/dislike")
async def dislike(request: Request):
    # 获取请求体中的数据
    request_body = await request.json()
    # 获取用户ID
    userId = user_management.get_user_id_by_token(
        "./db/users.db", request.headers.get("token"), get_db_cursor()
    )
    user_id = userId[0]
    # 广告ID
    ads_id = request_body.get("ads_id")

    db = user_management.dislike_ads_to_db(user_id, ads_id, get_db_cursor())
    # 返回响应
    return SuccessResponseData(data= db, msg='操作成功')


@app.post("/users/dragAndDrop")
async def dragAndDrop(request: Request):
    #TODO: 实现此接口
    request_body = await request.json()
    # 获取用户ID
    userId = user_management.get_user_id_by_token(
        "./db/users.db", request.headers.get("token"), get_db_cursor())
    user_id = userId[0]
    # 广告ID组
    ads_id_list = request_body.get("ads_id_list")

    user_management.drag_and_drop_ads_to_db(user_id, ads_id_list, get_db_cursor())

    return SuccessResponseData(data="", msg='操作成功')


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
#schedule.every(10).seconds.do()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    schedule.run_pending()  # 运行所有可以运行的任务
    time.sleep(1)  # 等待一秒
    print("")
