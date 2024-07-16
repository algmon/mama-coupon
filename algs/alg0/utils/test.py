from YOLO_Segmentation import *
import matplotlib.pyplot as plt

# 加载YOLOv8语义分割模型（最小参数量）
model_path = 'config/weight/yolov8n-seg.pt'
model = load_model(model_path)

# 加载摄像头
cap = load_camera(1)

# 获取模型推理
out = camera_segmentation(model, cap)

# 根据两个点坐标截取人物画像图片
def save_one_person(xyxy, img):
    crop = img[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::(-1)]
    return crop

for box in out[0].boxes:
    person_img = save_one_person(box.xyxy, out[0].orig_img)


# 画出原始图像
# plt.imshow(out[0].orig_img)
# plt.show()

# 画出裁剪后的图片
plt.imshow(person_img)
plt.show()

# 显示结果
# cv2.imshow('frame', out)
# cv2.waitKey(0)

# 关闭摄像头
cap.release()

# 关闭窗口
# cv2.destroyAllWindows()
