import requests
import os

# AI评估人物图像(URL)
def eval_fashion_person(img_url):
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
                    "url": img_url
                    }
                }
                ]
            }
        ]
    }
    res = requests.post(url, json=body, headers=headers)
    if res.status_code == 200:
        reply_text = res.json().get("choices")[0]['message']['content']
        return reply_text
    else:
        error = res.json().get("error")
        print(f"请求异常, 错误码={res.status_code}, 错误类型={error.get('type')}, 错误信息={error.get('message')}")

if __name__ == '__main__':
    img_url = "https://res.cloudinary.com/djba6ta1n/image/upload/v1721106667/Beijing%20Road%20Crossing%20Walker/sample.1.jpg"
    print(eval_fashion_person(img_url))
