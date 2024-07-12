from fastapi import APIRouter
import requests
from fastapi import Request
# Import your user management module here
import user_management
import os
from common.resp import SuccessResponseData

api_aiChat = APIRouter()
LINKAI_KEY = os.environ["LINKAI_KEY"]
LINKAI_CODE = os.environ["LINKAI_CODE"]
# url
url = "https://api.link-ai.tech/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + LINKAI_KEY
}


@api_aiChat.post("/answer")
async def get_users(request: Request):
    print("key:"+LINKAI_KEY)
    print("code:"+LINKAI_CODE)
    data = await request.json()
    issue = data.get("issue")
    body = {
        "app_code": LINKAI_CODE,
        "messages": [
            {
                "role": "user",
                "content": issue
            }
        ]
    }
    print("body:", body)
    #  访问linkai
    res = requests.post(url, json=body, headers=headers)
    if res.status_code == 200:
        reply_text = res.json().get("choices")[0]['message']['content']
        print(reply_text)
    else:
        error = res.json().get("error")
        print(
            f"请求异常, 错误码={res.status_code}, 错误类型={error.get('type')}, 错误信息={error.get('message')}")

    return SuccessResponseData(data={"answer": reply_text}, msg='获取成功')
