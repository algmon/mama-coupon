from utils import *

# 使用摄像头进行语义分割
def camera_segmentation(model, cap, img_size=(1920,1088), save_txt=False, save_crop=False):

    # 读取摄像头内容
    _, input = cap.read()

    # 模型推理
    results = model(input, imgsz=img_size, save_txt=save_txt, save_crop=save_crop, classes=0)

    return results

# 循环读取摄像头推理
def reuse_camera_segmentation(model, camera_num=0, box=True, save_txt=False, save_crop=False):

    # 将模型加载到图形计算设备
    model = load_device(model)

    # 循环读取摄像头推理
    while True:

        # 读取摄像头
        cap = load_camera(camera_num)

        out = camera_segmentation(model, cap)

        # 显示结果(带框/不带框）
        if box:
            out = out[0].plot()
        else:
            out = out[0].plot(boxes=False)  # 不显示预测框

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
    model = load_model(model_path)
    # yaml_path = '../config/model/yolov8n-seg.yaml'
    # model = load_model(model_path, yaml_path)

    # 单次展示语义分割
    # cap = load_camera(1)
    # out = camera_segmentation(model, cap)

    # 展示实时语义分割
    reuse_camera_segmentation(model)