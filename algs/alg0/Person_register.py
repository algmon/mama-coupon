import unittest
from datetime import datetime

import schedule
from fastapi import FastAPI

from utils import *
from YOLO_segmentation import *
import sys
from pathlib import Path
import user_management

app = FastAPI()


#相关注册方法
def register_user_by_camera(username,avatar_url,fashion_score,fashion_eval_reason):

    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    last_updated_at = formatted_now
    is_active = "1"
    success = user_management.register_user_by_camera_to_db(
        "./db/users.db", username, last_updated_at, is_active, avatar_url, fashion_score, fashion_eval_reason,  app.state.db.cursor())

    if success:
        return {"message": "User Registration successful.", "code": 200}
    else:
        return {"message": "Registration failed."}, 400


# 使用摄像头发现行人并注册
def person_register():

    # 加载YOLOv8语义分割模型（最小参数量）
    model_path = '../config/weight/yolov8n-seg.pt'
    model = load_model(model_path)

    # 加载模型到图形计算设备
    model = load_device(model)

    # 暂存图片地址
    file_path = './temp.png'

    # 加载摄像头
    cap = load_camera(0)

    # 调用模型推理
    out = camera_segmentation(model, cap)

    for box in out[0].boxes:

        # 根据框截取人物图像
        person_img = get_one_person(box.xyxy, out[0].orig_img)

        # 将图片存为PNG文件
        save_img_as_png(person_img, file_path)

        # 获取图片名称
        img_name, person_name = get_one_name()

        # 将图片放到S3
        save_S3(img_name)

        # 从S3取出图片URL
        img_url = take_S3(img_name)

        # 获取图片的评分和评价
        score, conclusion = get_score_conclusion(img_url)

        # 进行被动用户注册
        register_user_by_camera (person_name, img_url, score, conclusion)

        # return person_name, img_url, score, conclusion

schedule.every(10).seconds.do(person_register())

if __name__ == '__main__':
    schedule.run_pending()  # 运行所有可以运行的任务
    time.sleep(1)  # 等待一秒
    print("")
    # print(person_name, img_url, score, conclusion)

