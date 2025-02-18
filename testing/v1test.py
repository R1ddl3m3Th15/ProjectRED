import os
import torch
from deepface import DeepFace
from torchvision import models, transforms
from PIL import Image
import cv2

# Base directory
BASE_DIR = r'D:/ProjectRED'
# Replace with your test image path
IMAGE_PATH = os.path.join(BASE_DIR, 'inputs', 'testkat.jpg')
MODEL_DIR = os.path.join(BASE_DIR, 'models')


def analyze_facial_attributes(image_path):
    """Analyze facial attributes using DeepFace."""
    try:
        print("\nAnalyzing facial attributes with DeepFace...")
        analysis_result = DeepFace.analyze(
            img_path=image_path,
            actions=['age', 'gender', 'emotion'],
            enforce_detection=False
        )
        result = analysis_result[0]  # DeepFace returns a list
        print("\n--- Facial Attribute Analysis Results ---")
        print(f"Age: {result['age']}")
        print(f"Gender: {result['dominant_gender']}")
        print(f"Emotion Scores: {result['emotion']}")
        print(f"Dominant Emotion: {result['dominant_emotion']}")
    except Exception as e:
        print(f"Error in facial attribute analysis: {e}")


def analyze_scene(image_path):
    """Analyze scene attributes using Places365."""
    try:
        print("\nAnalyzing scene with Places365...")
        # Load Places365 model
        scene_model = models.resnet50(num_classes=365)
        scene_model_file = os.path.join(
            MODEL_DIR, 'places365', 'resnet50_places365.pth.tar')
        checkpoint = torch.load(
            scene_model_file, map_location=torch.device('cpu'))
        state_dict = {k.replace('module.', ''): v for k,
                      v in checkpoint['state_dict'].items()}
        scene_model.load_state_dict(state_dict)
        scene_model.eval()

        # Image transformations
        preprocess = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        # Load scene categories
        categories_file = os.path.join(
            MODEL_DIR, 'places365', 'categories_places365.txt')
        with open(categories_file) as f:
            categories = [line.strip().split(' ')[0][3:] for line in f]
            categories = tuple(categories)

        # Analyze image
        img = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(img).unsqueeze(0)
        with torch.no_grad():
            output = scene_model(input_tensor)
            probabilities = torch.softmax(output, dim=1)
            top_probs, top_indices = probabilities.topk(5)

        print("\n--- Scene Recognition Results ---")
        for prob, idx in zip(top_probs[0], top_indices[0]):
            print(f"{categories[idx]}: {prob.item():.4f}")
    except Exception as e:
        print(f"Error in scene analysis: {e}")


def analyze_objects(image_path):
    """Analyze objects using YOLOv5."""
    try:
        print("\nAnalyzing objects with YOLOv5...")
        # Load YOLOv5 model
        yolov5_dir = os.path.join(MODEL_DIR, 'yolov5')
        model = torch.hub.load(yolov5_dir, 'yolov5s', source='local')
        model.eval()

        # Perform object detection
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = model(img_rgb)

        print("\n--- Object Detection Results ---")
        # Print detections as a pandas DataFrame
        print(results.pandas().xyxy[0])

        # Visualize results
        results.show()
    except Exception as e:
        print(f"Error in object detection: {e}")


def main():
    print("\nStarting Combined Analysis...")
    print(f"Processing Image: {IMAGE_PATH}")

    # DeepFace for facial attributes
    analyze_facial_attributes(IMAGE_PATH)

    # Places365 for scene recognition
    analyze_scene(IMAGE_PATH)

    # YOLOv5 for object detection
    analyze_objects(IMAGE_PATH)

    print("\nAnalysis Complete.")


if __name__ == '__main__':
    main()
