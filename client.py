import requests
import json
from PIL import Image
import base64

#Where the server runs
BASE_URL = "https://maximus-semidivided-annalise.ngrok-free.dev"
#How it logs into the server 
API_KEY = "secret123" 
#What it sends with each request
HEADERS = {
    "x-api-key": API_KEY,
}


def list_models():
    """Prints the available models."""
    try:
        response = requests.get(f"{BASE_URL}/v1/models", headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            print("\nAvailable modeller:")
            for model in data.get("models", []):
                print(" -", model)
        else:
            print("Server error:", response.status_code, response.text)

    except Exception as e:
        print("Couldn't connect to the server:", e)

def classify_review():
    """Semtiment of a comment"""
    text = input("\nLeave a comment: ")
    payload = {"text": text}

    try:
        response = requests.post(
            f"{BASE_URL}/v1/semantic",
            json=payload,
            headers=HEADERS,
        )

        if response.status_code == 200:
            data = response.json()
            label = data.get("label")
            confidence = data.get("confidence")
            print(f"\nSentiment: {label}")
            print(f"Confidence: {confidence}")
        else:
            print("Server Error:", response.status_code, response.text)
    except Exception as e:
        print("Couldn't connect to the server", e)
def classify_image():
    # Uploades an image and prints the classification 
    path = input("\nPath to image: ")

    try:
        with open(path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
        payload = {"image_base64": image_base64}
        response = requests.post(
            f"{BASE_URL}/v1/images", 
            json=payload,
            headers=HEADERS,
        )


        if response.status_code == 200:
            data = response.json()
            label = data.get("label")
            confidence = data.get("confidence")
            print("\nKlassifikation:", label)
            if confidence is not None:
                print("Confidence:", confidence)
        else:
            print("Server error:", response.status_code, response.text)

    except FileNotFoundError:
        print("Image not found - check the file path")
    except Exception as e:
        print("Couldn't connect to server:", e)
def classify_image_top5():
    path = input("\nPath to image: ")

    try:
        with open(path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        payload = {"image_base64": image_base64}
        response = requests.post(
            f"{BASE_URL}/v2/images", 
            json=payload,
            headers=HEADERS,
        )

        if response.status_code == 200:
            data = response.json()
            print("\nTop-5 predictions:\n")
            for p in data.get("predictions", []):
                print(f" - {p['label']} ({p['confidence']:.4f})")
        else:
            print("Server error:", response.status_code, response.text)
    except FileNotFoundError:
        print("Image not found — check the file path.")
    except Exception as e:
        print("Couldn't connect to server:", e)

def print_menu():
    print("\n--- AI Client Program ---")
    print("1. List available models")
    print("2. Classify text")
    print("3. Classify image")
    print("4. Classify image with top 5")
    print("5. End client")


def main():
    while True:
        print_menu()
        choice = input("\nChoose a function (1-5): ")

        if choice == "1":
            list_models()
        elif choice == "2":
            classify_review()
        elif choice == "3":
            classify_image()
        elif choice == "4":
            classify_image_top5()
        elif choice == "5":
            print("Ending client...")
            break
        else:
            print("Invalid – try again.")


if __name__ == "__main__":
    main()
