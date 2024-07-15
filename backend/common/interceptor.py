from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from fastapi.responses import JSONResponse


class Interceptor(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # 从请求头中获取 token
        token = request.headers.get("token")
        # 检查 token 是否存在
        if not token:
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        # 调用下一个请求处理函数
        response = await call_next(request)
        return response
