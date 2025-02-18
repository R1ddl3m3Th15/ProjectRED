import torch
from torchvision import models, transforms
from PIL import Image
import os

# Paths
BASE_DIR = r'D:/ProjectRED'
MODEL_DIR = os.path.join(BASE_DIR, 'models', 'places365')
IMAGE_PATH = os.path.join(BASE_DIR, 'inputs', 'test_img4.jpg')

# Load the pre-trained Places365 model


def load_places365_model():
    model = models.resnet50(num_classes=365)  # 365 categories in Places365
    model_file = os.path.join(MODEL_DIR, 'resnet50_places365.pth.tar')

    # Load the model weights
    checkpoint = torch.load(model_file, map_location=torch.device('cpu'))
    state_dict = {k.replace('module.', ''): v for k,
                  v in checkpoint['state_dict'].items()}
    model.load_state_dict(state_dict)
    model.eval()
    return model

# Load scene categories


def load_categories():
    categories_file = os.path.join(MODEL_DIR, 'categories_places365.txt')
    with open(categories_file) as f:
        categories = [line.strip().split(' ')[0][3:] for line in f]
    return tuple(categories)

# Preprocess the image


def preprocess_image(image_path):
    preprocess = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    img = Image.open(image_path).convert('RGB')
    return preprocess(img).unsqueeze(0)

# Perform inference


def predict_scene(model, input_tensor, categories):
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        top_probs, top_indices = probabilities.topk(5)
        return top_probs, top_indices

# Main function


def main():
    print("Loading Places365 model...")
    model = load_places365_model()
    categories = load_categories()

    print("Preprocessing image...")
    input_tensor = preprocess_image(IMAGE_PATH)

    print("Predicting scene...")
    top_probs, top_indices = predict_scene(model, input_tensor, categories)

    print("\nTop 5 Scene Predictions:")
    for prob, idx in zip(top_probs[0], top_indices[0]):
        print(f"{categories[idx]}: {prob.item():.4f}")


if __name__ == '__main__':
    main()
