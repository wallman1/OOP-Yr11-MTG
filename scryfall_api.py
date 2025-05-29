import requests

def search_cards(query):
    url = f"https://api.scryfall.com/cards/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    return []