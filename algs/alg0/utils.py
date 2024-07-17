import cv2
from ultralytics import YOLO
import torch
from PIL import Image
import yaml
import boto3

from Snowflake import *
from Eval_fashion_person import *

# 读取摄像头（返回图片）
def load_camera(num, width=1920, height=1080):
    cap = cv2.VideoCapture(num)

    # 设置摄像头参数
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height);

    return cap

# 读取视频
def load_video(video_path):
    video = cv2.VideoCapture(video_path)
    return video

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

# 根据两个点坐标截取人物画像图片
def get_one_person(xyxy, img):
    crop = img[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::(-1)]
    return crop

# 保存图像
def save_img_as_png(img, file_path):
    Image.fromarray(img[..., ::-1]).save(file_path, format='PNG', quality=100, subsampling=0)

# 获取人物名称
def get_one_name():
    # 获取雪花算法对象
    snowflake = Snowflake(datacenter_id=1, worker_id=3)
    # 调用雪花算法获取文件名
    randID = snowflake.generate()
    randID = str(randID)
    file_name = f'{randID}.png'
    return file_name, randID

# 上传文件到S3
def save_S3(file_name):
    # 设置暂缓存图片地址
    file_path = './temp.png'

    # 读取S3的配置
    f = open('./config/S3/S3.yaml', 'r', encoding='utf-8')
    res = yaml.load(f, Loader=yaml.FullLoader)

    # 配置S3的访问信息
    access_key = res['access_key']
    secret_key = res['secret_key']

    # 创建S3资源对象
    s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # 获取桶对象
    bucket = s3.Bucket('fashion-imgs')

    # 设置元数据格式（避免获取URL时变成下载）
    metadata = {'Content-Type': 'image/png'}

    # 上传文件
    bucket.upload_file(file_path, file_name, ExtraArgs={'ContentType': 'image/png'})

# 从S3取出文件
def take_S3(img_name='person1.png'):
    # 读取配置
    f = open('./config/S3/S3.yaml', 'r', encoding='utf-8')
    res = yaml.load(f, Loader=yaml.FullLoader)

    # 配置S3的访问信息
    access_key = res['access_key']
    secret_key = res['secret_key']

    # 创建S3资源对象
    s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # 获取桶对象
    bucket = s3.Bucket('fashion-imgs')

    # 获取对象的URL
    img_url = s3.meta.client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 'fashion-imgs',
            'Key': img_name
        }
    )
    return img_url

# 从字符串获取其中的第一个数字
def extract_first_number(s):
    for char in s:
        if char.isdigit():
            return int(char)
    return -1  # 如果字符串中没有数字，返回-1

# 获取分数和评语
def get_score_conclusion(img_url):
    conclusion = eval_fashion_person(img_url)
    score = extract_first_number(conclusion)
    return score, conclusion
