from utils import *
from YOLO_segmentation import *
import sys
import os

# 获取上级两级目录的路径
parent_dir = os.path.dirname(os.path.dirname('backend/app.py'))

# 将上级目录添加到模块搜索路径
sys.path.append(parent_dir)

# from ....backend import register_user_by_camera

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
    cap = load_camera(1)

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
        # register_user_by_camera (person_name, img_url, score, conclusion)

        # return person_name, img_url, score, conclusion

if __name__ == '__main__':
    person_register()
    # print(person_name, img_url, score, conclusion)

