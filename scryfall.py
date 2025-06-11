# scryfall.py
import requests
import os
import time

ASSETS_DIR = "assets"

def get_card_data(card_name, retries=3, delay=1):
    url = f"https://api.scryfall.com/cards/named?exact={card_name}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Attempt {attempt+1} failed for {card_name}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Giving up on {card_name}")
                return None

def download_card_image(card_name):
    data = get_card_data(card_name)
    if not data or 'image_uris' not in data:
        return None

    image_url = data['image_uris']['normal']
    image_path = os.path.join(ASSETS_DIR, f"{card_name}.jpg")

    if not os.path.exists(image_path):
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as f:
            f.write(img_data)

    return image_path
