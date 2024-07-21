import logging
import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import mama_coupon_platform_management
import mama_coupon_developer_management
import mama_coupon_producers_management
import mama_coupon_consumer_management
import mama_coupon_recommendation_management

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

# 应用程序启动事件
# app startup event
@app.on_event("startup")
async def startup_event():
    # 使用 app.state 来存储数据库连接
    app.state.db = get_db_connection()
    logging.info("DB started successfully.")
    logging.info("App started successfully.")

# 应用程序关闭事件
# app shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    # 检查数据库连接是否存在，并且关闭它
    db = app.state.db
    if db and not db.is_connected():
        db.close()
    logging.info("DB shutdown successfully.")
    logging.info("App shutdown successfully.")

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
    return {"message": "欢迎你来到妈妈折扣券产品平台后端! 注：/docs可看到我们目前向外提供的API接口"}

# Mama Coupon Management

# Mama Coupon Platform Management
@app.post("/platform/get_public_coupon_feed")
async def get_public_coupon_feed(request: Request, db: cursor.MySQLCursor = Depends(get_db_cursor)):
    """
    Returns a list of matches for the target user group given time & location.

    Args:
        

    Returns:
        A JSON response with a list of coupons.
    """
    logging.info(f"get_public_coupon_feed endpoint accessed.")

    matches = mama_coupon_recommendation_management.get_public_coupon_feed()
    return {"matches": matches}

# Mama Coupon Provider Management
@app.post("/producers/produce_a_coupon")
async def produce_a_coupon(request: Request, db: cursor.MySQLCursor = Depends(get_db_cursor)):
    """
    Produce a Coupon on the platform.

    Args:
        prompt:
        negative_prompt:
        seed:

    Returns:
        A JSON response with the status of the creation.
    """
    logging.info("Provider Create endpoint accessed.")

    try:
        # Get data from the request body
        json_data = await request.json()
        prompt = json_data.get('prompt')
        negative_prompt = json_data.get('negative_prompt')
        seed = json_data.get('seed')

        # Get the MAMA_API_KEY from the request headers
        mama_api_key = request.headers.get("MAMA_API_KEY")     

        # Check if the MAMA_API_KEY is provided
        if not mama_api_key:
            return ErrorResponseData(401, "MAMA_API_KEY is required.")

        # Validate the MAMA_API_KEY
        developer_info = mama_coupon_developer_management.get_developer_by_key(mama_api_key, db)
        if not developer_info:
            return ErrorResponseData(401, "Invalid MAMA_API_KEY.")
        else:
            # log the developer info
            developer_name = developer_info[1]  # Assuming developer name is at index 1
            score_left = developer_info[5]  # Assuming score left is at index 2
            logging.info(f"Developer {developer_name} use API key to login, score left: {score_left}")

        success = mama_coupon_producers_management.create(
            prompt, negative_prompt, seed, mama_api_key)

        if success:
            return JSONResponse(
                status_code=200,
                content={"message": "Coupon created successfully.",
                         "code": 200, "data": {}}
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"message": "Coupon creation failed."}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error creating coupon: {e}"}
        )

# Mama Coupon Consumer Management
@app.post("/consumers/consume_a_coupon")
async def consume_a_coupon(request: Request, db: cursor.MySQLCursor = Depends(get_db_cursor)):
    # TODO: Implement this function
    pass

# Mama Coupon Recommendation Management

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)