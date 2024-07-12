from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
import os
import requests
from fastapi import Request
# Import your user management module here
from starlette.responses import JSONResponse

import user_management
# from app import get_matches_for_specifc_user
from common.resp import SuccessResponseData

api_fashion_video = APIRouter()


# 设置视频文件的本地路径
VIDEO_DIR = "E:\\business\\sfmm\\suanfamama-platform-common\\frontend\\img"
VIDEO_FILENAME = "1.mp4"  # 视频文件名称

# @api_fashion_video.get("/getVideo")
# async def get_video():
#     video_path = os.path.join(VIDEO_DIR, VIDEO_FILENAME)
#     if not os.path.isfile(video_path):
#         # 修正错误信息的引号为英文引号
#         return JSONResponse(status_code=404, content={"error": "Video not found"})
#
#     # 确保文件存在后，使用 StreamingResponse 来流式传输视频
#     return SuccessResponseData((StreamingResponse(open(video_path, 'rb'), media_type="video/mp4")),msg='获取成功')

#
# @api_fashion_video.get("/getVideo")
# async def get_video(advIds: str = Depends(get_matches_for_specifc_user)):
#     print(advIds)
#     # for advId in advIds.:
#
#     # 确保文件存在后，使用 StreamingResponse 来流式传输视频
#     return SuccessResponseData(msg='获取成功')
