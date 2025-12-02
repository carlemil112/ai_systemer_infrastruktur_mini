import requests
import json
from PIL import Image
import base64

#Hvor serveren kører (localthost)
BASE_URL = "http://192.168.0.170:8000"
#Hvordan den logger ind på serveren (her med en API-nøgle)
API_KEY = "secret123" 
#Hvad den sender med hver forespørgsel til serveren
HEADERS = {
    "x-api-key": API_KEY,
}

def list_models():
    """Henter og printer de modeller, som serveren stiller til rådighed."""
    try:
        response = requests.get(f"{BASE_URL}/v1/models", headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            print("\nTilgængelige modeller:")
            for model in data.get("models", []):
                print(" -", model)
        else:
            print("Fejl fra serveren:", response.status_code, response.text)

    except Exception as e:
        print("Kunne ikke forbinde til serveren:", e)

def classify_review():
    """Vurderer om en anmeldelse er positiv eller negativ"""
    text = input("\nSkriv din anmeldelse her: ")
    payload = {"text": text}

    try:
        response = requests.post(
            f"{BASE_URL}/v1/classify-review",
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
            print("Fejl fra serveren:", response.status_code, response.text)
    except Exception as e:
        print("Kunne ikke forbinde til serveren:", e)
def classify_image():
    """Uploader et billede til API'et og printer klassifikationen."""
    path = input("\nSti til billede (fx images/happy.jpg): ")

    try:
        with open(path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
        payload = {"image_base64": image_base64}
        response = requests.post(
            f"{BASE_URL}/v1/classify-image", 
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
            print("Fejl fra serveren:", response.status_code, response.text)

    except FileNotFoundError:
        print("Billedet blev ikke fundet – tjek stien.")
    except Exception as e:
        print("Kunne ikke forbinde til serveren:", e)
def print_menu():
    print("\n--- AI Client Program ---")
    print("1. List tilgængelige modeller")
    print("2. Klassificer tekst")
    print("3. Klassificér billede")
    print("4. Afslut")


def main():
    while True:
        print_menu()
        choice = input("\nVælg en funktion (1-4): ")

        if choice == "1":
            list_models()
        elif choice == "2":
            classify_review()
        elif choice == "3":
            classify_image()
        elif choice == "4":
            print("Afslutter klienten...")
            break
        else:
            print("Ugyldigt valg – prøv igen.")


if __name__ == "__main__":
    main()
