from YOLO_Segmentation import *

model_path = '../config/weight/yolov8n-seg.pt'
model = load_model(model_path)
input = '../data/exp1.in/sample.1.png'
results = model(input)
print(results)
