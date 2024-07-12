# resp.py
from fastapi import status
from fastapi.responses import JSONResponse  # , ORJSONResponse
from pydantic import BaseModel
from typing import Union, Optional

from common.error_code import ErrorBase


class respJsonBase(BaseModel):
    code: int
    msg: str
    data: Union[dict, list]


def SuccessResponseData(data: Union[list, dict, str] = None, msg: str = "Success"):
    """ 接口成功返回 """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 20000,
            'msg': msg,
            'data': data or {}
        }
    )


def ErrorResponseData(code: str, msg: Optional[str] = None,
                      data: Union[list, dict, str] = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """ 错误接口返回 """
    return JSONResponse(
        status_code=status_code,
        content={
            'code': code,
            'msg': msg,
            'data': data or {}
        }
    )
