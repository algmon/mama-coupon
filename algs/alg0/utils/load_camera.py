import cv2

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