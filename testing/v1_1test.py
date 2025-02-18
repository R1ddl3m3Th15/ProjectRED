import os
import cv2
import torch
from deepface import DeepFace
from torchvision import models, transforms
from PIL import Image
from collections import Counter

# Paths
BASE_DIR = r'D:/ProjectRED'
# Replace with your test video path
VIDEO_PATH = os.path.join(BASE_DIR, 'inputs', 'test_video2.mp4')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
MODEL_DIR = os.path.join(BASE_DIR, 'models')


def extract_frames(video_path, temp_dir):
    """Extract frames from the video and save them in the temp directory."""
    os.makedirs(temp_dir, exist_ok=True)
    print("\nExtracting frames from video...")
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    success, image = cap.read()
    while success:
        frame_path = os.path.join(temp_dir, f"frame_{frame_count:05d}.jpg")
        cv2.imwrite(frame_path, image)
        success, image = cap.read()
        frame_count += 1
    cap.release()
    print(f"Extracted {frame_count} frames.")
    return frame_count


def analyze_facial_attributes(image_path, emotion_counter):
    """Analyze facial attributes for a single frame and update the emotion counter."""
    try:
        analysis_result = DeepFace.analyze(
            img_path=image_path,
            actions=['emotion'],
            enforce_detection=False
        )
        dominant_emotion = analysis_result[0]['dominant_emotion']
        emotion_counter[dominant_emotion] += 1
    except Exception as e:
        print(f"Error in facial attribute analysis for {image_path}: {e}")


def analyze_scene(image_path, scene_counter, categories, scene_model, preprocess):
    """Analyze scene attributes for a single frame and update the scene counter."""
    try:
        img = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(img).unsqueeze(0)
        with torch.no_grad():
            output = scene_model(input_tensor)
            probabilities = torch.softmax(output, dim=1)
            _, top_indices = probabilities.topk(1)
            scene_label = categories[top_indices[0][0]]
            scene_counter[scene_label] += 1
    except Exception as e:
        print(f"Error in scene analysis for {image_path}: {e}")


def analyze_objects(image_path, object_counter, model):
    """Analyze objects for a single frame and update the object counter."""
    try:
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = model(img_rgb)
        detected_objects = results.pandas().xyxy[0]['name'].tolist()
        object_counter.update(detected_objects)
    except Exception as e:
        print(f"Error in object detection for {image_path}: {e}")


def main():
    print("\nStarting Video Analysis...")
    print(f"Processing Video: {VIDEO_PATH}")

    # Step 1: Extract frames
    frame_count = extract_frames(VIDEO_PATH, TEMP_DIR)

    # Step 2: Prepare models and counters
    print("\nLoading models...")
    # DeepFace for facial attributes
    emotion_counter = Counter()

    # Places365 for scene recognition
    scene_model = models.resnet50(num_classes=365)
    scene_model_file = os.path.join(
        MODEL_DIR, 'places365', 'resnet50_places365.pth.tar')
    checkpoint = torch.load(scene_model_file, map_location=torch.device('cpu'))
    state_dict = {k.replace('module.', ''): v for k,
                  v in checkpoint['state_dict'].items()}
    scene_model.load_state_dict(state_dict)
    scene_model.eval()

    # Scene categories and preprocessing
    categories_file = os.path.join(
        MODEL_DIR, 'places365', 'categories_places365.txt')
    with open(categories_file) as f:
        categories = [line.strip().split(' ')[0][3:] for line in f]
        categories = tuple(categories)
    preprocess = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    scene_counter = Counter()

    # YOLOv5 for object detection
    yolov5_dir = os.path.join(MODEL_DIR, 'yolov5')
    object_model = torch.hub.load(yolov5_dir, 'yolov5s', source='local')
    object_model.eval()
    object_counter = Counter()

    # Step 3: Analyze each frame
    print("\nAnalyzing frames...")
    for i in range(frame_count):
        frame_path = os.path.join(TEMP_DIR, f"frame_{i:05d}.jpg")
        if not os.path.exists(frame_path):
            continue
        print(f"Analyzing Frame {i+1}/{frame_count}...")

        # Analyze facial attributes
        analyze_facial_attributes(frame_path, emotion_counter)

        # Analyze scene attributes
        analyze_scene(frame_path, scene_counter,
                      categories, scene_model, preprocess)

        # Analyze objects
        analyze_objects(frame_path, object_counter, object_model)

    # Step 4: Display cumulative results
    print("\n--- Cumulative Results ---")

    print("\nFacial Emotions:")
    for emotion, count in emotion_counter.most_common():
        print(f"{emotion}: {count}")

    print("\nScenes:")
    for scene, count in scene_counter.most_common():
        print(f"{scene}: {count}")

    print("\nObjects:")
    for obj, count in object_counter.most_common():
        print(f"{obj}: {count}")

    print("\nVideo Analysis Complete.")


if __name__ == '__main__':
    main()
