import torch
import cv2
from matplotlib import pyplot as plt

# Load YOLOv5 model
model = torch.hub.load('D:\ProjectRED\models\yolov5',
                       'yolov5s', source='local')
model.eval()

# Read an image
img_path = r'D:\ProjectRED\inputs\test_img.jpg'  # Replace with your image path
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Inference
results = model(img_rgb)

# Print detected objects
print(results.pandas().xyxy[0])

# Display results
results.show()
