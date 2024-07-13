import json
import os
import torch

# 1. Data
base = "./data/exp1.in"

# Get a list of all the files in the directory
imgs = os.listdir(base)

# Add the file path base to the list of images
imgs = [os.path.join(base, img) for img in imgs]

# Print the list of files
print(imgs)

# 2. Model
# TODO: Try yolov8 instead of yolov5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Images
# imgs = ['./data/sample.1.png']  # batch of images

# Inference
results = model(imgs)

# Results
results.print()
results.save()  # or .show()

for i in range(0,len(imgs)):
    print("img #:", i)
    results.xyxy[i]  # img1 predictions (tensor)
    print(results.pandas().xyxy[i])  # img1 predictions (pandas)
    print()
