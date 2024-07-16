from YOLO_Segmentation import *

import sys
import os
sys.path.append(os.path.abspath('.../alg6'))
from ..alg6.talk_to_ling import *

# 根据两个点坐标截取人物画像图片
def save_one_person(xyxy, img):
    crop = img[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::(-1)]
    return crop

def result_process():
    # 加载YOLOv8语义分割模型（最小参数量）
    model_path = 'config/weight/yolov8n-seg.pt'
    model = load_model(model_path)
    yaml_path = '../config/model/yolov8n-seg.yaml'
    # model = load_model(model_path, yaml_path)
    model = load_device(model)

    # 加载摄像头
    cap = load_camera(1)

    # 调用模型推理
    out = camera_segmentation(model, cap)

    for box in out[0].boxes:
        person_img = save_one_person(box.xyxy, out[0].orig_img)
        eval_fashion_person()

result_process()
