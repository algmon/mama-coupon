import requests
import os

def say_hi(query):
    url = os.environ["LINKAI_HOST"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["LINKAI_KEY"]
    }
    body = {
        "app_code": os.environ["LINKAI_CODE_2"],
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }
    res = requests.post(url, json=body, headers=headers)
    if res.status_code == 200:
        reply_text = res.json().get("choices")[0]['message']['content']
        print("AI时尚买手张优玲:", reply_text)
    else:
        error = res.json().get("error")
        print(f"请求异常, 错误码={res.status_code}, 错误类型={error.get('type')}, 错误信息={error.get('message')}")

def eval_fashion_person():
    url = os.environ["LINKAI_HOST"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["LINKAI_KEY"]
    }
    body = {
        "app_code": os.environ["LINKAI_CODE_2"],
        "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": "图中人物的穿搭时尚吗？"
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1721106667/Beijing%20Road%20Crossing%20Walker/sample.1.jpg"
                    }
                }
                ]
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

#query="您好，请问目前你有什么重要的时尚法则？"
query="您好，我想咨询一下什么才是您心中真正的时尚？"
print(f"算法妈妈助理小妈妈: {query}")
say_hi(query)
#eval_fashion_person()