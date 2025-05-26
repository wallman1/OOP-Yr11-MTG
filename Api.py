import scrython
import requests
import time
from requests import get
from json import loads
from shutil import copyfileobj

def Searchcard(getCard):
    try:
        card = scrython.cards.Named(fuzzy=getCard)
        if card.object() == 'error':
            print(card.scryfallJson['details'])

        if "Creature" in card.type_line():
            PT = "({}/{})".format(card.power(), card.toughness())
        else:
            PT = ""

        if card.cmc() == 0:
            mana_cost = ""
        else:
            mana_cost = card.mana_cost()

        string = """
        {cardname} {mana_cost}
        {type_line} {set_code} {rarity}
        {oracle_text}{power_toughness}
        """.format(
                cardname=card.name(),
                mana_cost=mana_cost,
                type_line=card.type_line(),
                set_code=card.set_code().upper(),
                rarity=card.rarity(),
                oracle_text=card.oracle_text(),
                power_toughness=PT
                )

        return(string)

    except:
        print("404 Card Not Found")

    IMAGE_PATH = "Documents\GitHub\OOP-Yr11-MTG" # You can replace this with whatever path

    def save_image(path, url, name):
        response = requests.get(url)

        with open('{}{}.png'.format(path, name), 'wb') as f:
            f.write(response.content)

    def get_all_pages(set_code):
        page_count = 1
        all_data = []
        while True:
            time.sleep(0.5)
            page = scrython.cards.Search(q='e:{}'.format(set_code), page=page_count)
            all_data = all_data + page.data()
            page_count += 1
            if not page.has_more():
                break

        return all_data

    def get_all_cards(card_array):
        card_list = []
        for card in card_array:
            time.sleep(0.5)
            id_ = card['id']
            card = scrython.cards.Id(id=id_)
            card_list.append(card)
        return card_list

def get_image(name):
    card = scrython.cards.Named(fuzzy=name)
    cardname=card.name()
    card = loads(get(f"https://api.scryfall.com/cards/search?q={cardname}").text)
 
    # Get the image URL
    img_url = card['data'][0]['image_uris']['png']
        
    # Save the image
    with open('image.png', 'wb') as out_file:
        copyfileobj(get(img_url, stream = True).raw, out_file)

class creature():
    def __init__(self):
        pass

    def haste():
        pass

    def detain():
        pass

    def evolve():
        pass

    def hexproof():
        pass

    def amass():
        pass

    def flying():
        pass

    def reach():
        pass

    def deathtouch():
        pass

    def doublestrike():
        pass

    def firststrike():
        pass

    def trample():
        pass

    def defender():
        pass

    def lifelink():
        pass

    def menace():
        pass

    def vigilance():
        pass