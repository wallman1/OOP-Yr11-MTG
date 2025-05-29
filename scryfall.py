# scryfall.py
import requests
import os

ASSETS_DIR = "assets"
def get_card_data(card_name):
    response = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}")
    if response.status_code != 200:
        print(f"Card not found: {card_name}")
        return None
    return response.json()

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
