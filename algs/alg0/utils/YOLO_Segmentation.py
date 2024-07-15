import cv2
from ultralytics import YOLO
import torch

from load_camera import *

# 加载模型
def load_model(model_path, yaml_path=None, task='segment'):

    # 加载（改动过结构）的模型
    if yaml_path:
        model = YOLO(yaml_path, task=task).load(model_path)
    else:
        model = YOLO(model_path, task=task)
    return model

# 加载模型到图形计算设备
def load_device(model):

    # 获取图形计算设备信息
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    # 将模型切换到图形计算设备上
    model.to(device)

    return model

# 使用摄像头进行语义分割
def camera_segmentation(model, cap, box=True):

    # 读取摄像头内容
    _, input = cap.read()

    # 模型推理
    results = model(input, save_txt=True, save_crop=True, classes=0)

    # 显示结果(带框/不带框）
    if box:
        out = results[0].plot()
    else:
        out = results[0].plot(boxes=False)  # 不显示预测框

    return out

# 循环读取摄像头推理
def reuse_camera_segmentation(model, camera_num=1, box=True):

    # 将模型加载到图形计算设备
    model = load_device(model)

    # 循环读取摄像头推理
    while True:

        # 读取摄像头
        cap = load_camera(camera_num)

        out = camera_segmentation(model, cap,box=box)

        # 显示结果
        cv2.imshow('frame', out)

        # 等待退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关闭摄像头
    cap.release()

    # 关闭窗口
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # 加载YOLOv8语义分割模型（最小参数量）
    model_path = '../config/weight/yolov8n-seg.pt'
    yaml_path = '../config/model/yolov8n-seg.yaml'
    model = load_model(model_path)
    # model = load_model(model_path, yaml_path)

    cap = load_camera(1)
    out = camera_segmentation(model, cap, box=True)
    # 显示结果
    cv2.imshow('frame', out)
    cv2.waitKey(0)

    # 关闭摄像头
    cap.release()

    # 关闭窗口
    cv2.destroyAllWindows()