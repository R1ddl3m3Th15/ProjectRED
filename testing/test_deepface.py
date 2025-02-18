from deepface import DeepFace
import os

# Path to the test image
BASE_DIR = r'D:/ProjectRED'
# Replace with your test image path
IMAGE_PATH = os.path.join(BASE_DIR, 'inputs', 'test_img6.jpg')


def analyze_facial_attributes(image_path):
    try:
        # Perform facial attribute analysis
        print("Analyzing facial attributes...")
        analysis_result = DeepFace.analyze(
            img_path=image_path,
            actions=['age', 'gender', 'emotion'],
            enforce_detection=False
        )

        # DeepFace.analyze returns a list, so access the first element
        result = analysis_result[0]

        print("\nFacial Attribute Analysis Result:")
        print(result)

        # Print individual results for better readability
        print("\n--- Detailed Results ---")
        print(f"Age: {result['age']}")
        print(f"Gender: {result['dominant_gender']}")
        print(f"Emotion Scores: {result['emotion']}")
        print(f"Dominant Emotion: {result['dominant_emotion']}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    analyze_facial_attributes(IMAGE_PATH)
