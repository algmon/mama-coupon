import requests
import os

url = os.environ["LINKAI_HOST"]
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.environ["LINKAI_KEY"]
}
body = {
    "app_code": os.environ["LINKAI_CODE_1"],
    "messages": [
        {
            "role": "user",
            "content": "你好，有江纬和算法妈妈的简介吗？"
        }
    ]
}
res = requests.post(url, json=body, headers=headers)
if res.status_code == 200:
    reply_text = res.json().get("choices")[0]['message']['content']
    print(reply_text)
else:
    error = res.json().get("error")
    print(f"请求异常, 错误码={res.status_code}, 错误类型={error.get('type')}, 错误信息={error.get('message')}")