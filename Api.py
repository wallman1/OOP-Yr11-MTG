import scrython
import requests
import time
import json
import os
from shutil import copyfileobj
from requests import get

DECK_FILE = "deck.json"

def search_cards(query):
    print("start code")
    try:
        response = scrython.cards.Search(q=query)
        return response.data()
    except Exception as e:
        print("Search failed:", e)
        return []

def search_cards_exact(query):
    try:
        response = scrython.cards.Search(exact=query)
        return response.data()
    except Exception as e:
        print("Search failed:", e)
        return []

def get_image_from_url(url):
    try:
        response = get(url, stream=True)
        if response.status_code == 200:
            with open("image.png", "wb") as out_file:
                copyfileobj(response.raw, out_file)
            return True
    except Exception as e:
        print("Image download failed:", e)
    return False

def save_to_deck(card_name):
    print("start code")
    deck = []
    if os.path.exists(DECK_FILE):
        with open(DECK_FILE, "r") as f:
            try:
                deck = json.load(f)
            except json.JSONDecodeError:
                deck = []
                print("card was not added")

    deck.append(card_name)

    with open(DECK_FILE, "w") as f:
        json.dump(deck, f)

def load_deck():
    if os.path.exists(DECK_FILE):
        with open(DECK_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
