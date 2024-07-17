import requests
import json
import os

query = "你好，我想给广州算法妈妈技术有限公司设计一组广告，放在广州地铁的广告灯箱上" # 咨询内容
print(f"算法妈妈助理小妈妈: {query}")
url = os.environ["COZE_HOST"]
headers = {
    "Authorization": "Bearer " + os.environ["COZE_API_KEY"],
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Host": "api.coze.cn",
    "Connection": "keep-alive"
}
body = {
    "conversation_id": "0",
    "bot_id": os.environ["COZE_BOT_ID"],
    "user": "0",
    "query": query,
    "stream": False
}

res = requests.post(url, json=body, headers=headers)

if res.status_code == 200:
    #reply_text = res.json().get("choices")[0]['message']['content']
    #print(reply_text)

    # Parse the JSON response
    response_data = res.json()
    # Find the message with "type" as "answer"
    answer_message = next(
        (message for message in response_data["messages"] if message["type"] == "answer"),
        None,
    )
    # Extract the answer content
    if answer_message:
        answer = answer_message["content"]
        print(f"胡兆基顾问: {answer}")
    else:
        print("No answer found in the response.")

else:
    error = res.json().get("error")
    print(f"请求异常, 错误码={res.status_code}, 错误类型={error.get('type')}, 错误信息={error.get('message')}")
