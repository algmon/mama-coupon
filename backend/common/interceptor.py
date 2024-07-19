from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from fastapi.responses import JSONResponse
from user_management import get_user_id_by_token, get_user_by_developer_token
from common.db import get_db_connection
import base64

class Interceptor(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        token1 = request.headers.get("Token")
        db = get_db_connection()
        # 放行api
        doJson = {"/users/login", "/users/register", "/docs", "/openapi.json"}
        for url in doJson:
            if request.url.path == url:
                response = await call_next(request)
                return response

        # 处理OPTIONS请求
        if request.method == "OPTIONS":
            response = JSONResponse(status_code=200, content={})
            response.headers["Access-Control-Allow-Origin"] = "http://localhost:9527"
            response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, token, mama_api_key"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response

        mama_api_key = request.headers.get("mama_api_key")
        if mama_api_key is not None:
            mama_api_key_bytes = mama_api_key.encode('utf-8')
            mama_api_key_base64 = base64.b64encode(mama_api_key_bytes)
            userInfo = get_user_by_developer_token(mama_api_key_base64, db.cursor())
            # 检查 token 是否存在
            if userInfo:
                # 调用下一个请求处理函数
                response = await call_next(request)
                response.headers["Access-Control-Allow-Origin"] = "http://localhost:9527"
                response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
            else:
                return JSONResponse(status_code=401, content={"message": "Unauthorized of developer"})
        else:
            # 普通用户
            token = request.headers.get("token")
            # 如果token不为空
            if token:
                userId = get_user_id_by_token("", token, db.cursor())
                print("登录成功userId:" + userId[0])
                # 检查 token 是否存在
                if userId:
                    # 调用下一个请求处理函数
                    response = await call_next(request)
                    response.headers["Access-Control-Allow-Origin"] = "http://localhost:9527"
                    response.headers["Access-Control-Allow-Credentials"] = "true"
                    return response
                else:
                    return JSONResponse(status_code=401, content={"message": "Unauthorized of user"})

            else:
                return JSONResponse(status_code=401, content={"message": "Unauthorized of user"})
