import pygame
import requests
from scryfall_api import search_cards
from Cards import Card
from Deck import Deck
from io import BytesIO
import json
import os
from scryfall import download_card_image
from Cards import Card


pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("MTG Tabletop Simulator")
font = pygame.font.SysFont("Arial", 20)
input_font = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BG_COLOR = (30, 30, 30)
LIGHT_GRAY = (80, 80, 80)

CARD_HEIGHT = 40
VISIBLE_CARDS = 15
CARD_WIDTH, CARD_DISPLAY_HEIGHT = 100, 140
image_cache = {}

def get_card_image(url):
    if url in image_cache:
        return image_cache[url]
    try:
        response = requests.get(url)
        img = pygame.image.load(BytesIO(response.content))
        image_cache[url] = img
        return img
    except:
        return None
    
def load_deck_from_file(file_path="my_deck.json"):
    if not os.path.exists(file_path):
        print("Deck file not found.")
        return []

    with open(file_path, "r") as f:
        names = json.load(f)

    deck = []
    for name in names:
        image_path = download_card_image(name)
        # Use dummy stats for now — can extend this with Scryfall JSON data
        card = Card(name, power=2, toughness=2)
        deck.append(card)
    return deck

def render_text(text, x, y, font=font, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_input_box(input_text, active):
    color = YELLOW if active else GRAY
    pygame.draw.rect(screen, color, (20, 20, 400, 40), 2)
    txt_surface = input_font.render(input_text, True, WHITE)
    screen.blit(txt_surface, (25, 25))

def draw_card_list(cards, start_index, selected_index):
    for i, card in enumerate(cards[start_index:start_index + VISIBLE_CARDS]):
        y = 80 + i * CARD_HEIGHT
        color = YELLOW if i + start_index == selected_index else GRAY
        pygame.draw.rect(screen, LIGHT_GRAY, (20, y, 400, CARD_HEIGHT), 0)
        render_text(card.name, 25, y + 10, color=color)

def draw_hand(hand):
    for i, card in enumerate(hand):
        img = get_card_image(card.image_url)
        if img:
            img = pygame.transform.scale(img, (CARD_WIDTH, CARD_DISPLAY_HEIGHT))
            screen.blit(img, (300 + i * (CARD_WIDTH + 10), 750))

def draw_table(table_cards):
    for card in table_cards:
        img = get_card_image(card.image_url)
        if img:
            img = pygame.transform.scale(img, (CARD_WIDTH, CARD_DISPLAY_HEIGHT))
            screen.blit(img, card.rect.topleft)

def main():
    running = True
    clock = pygame.time.Clock()

    input_text = ""
    input_active = False
    deck = Deck()

    selected_card_index = 0
    search_scroll = 0

    battlefield = []
    hand = []

    dragging_card = None
    offset_x, offset_y = 0, 0

    query = "lightning bolt"
    cards_data = search_cards(query)
    card_objects = [Card(c["name"], c["image_uris"]["normal"], c["mana_cost"], c["type_line"]) for c in cards_data if "image_uris" in c]

    while running:
        screen.fill(BG_COLOR)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        query = input_text
                        input_text = ""
                        cards_data = search_cards(query)
                        card_objects = [Card(c["name"], c["image_uris"]["normal"], c["mana_cost"], c["type_line"]) for c in cards_data if "image_uris" in c]
                        selected_card_index = 0
                        search_scroll = 0
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                else:
                    if event.key == pygame.K_h and card_objects:
                        hand.append(card_objects[selected_card_index])
                    if event.key == pygame.K_b and card_objects:
                        card = card_objects[selected_card_index]
                        card.rect = pygame.Rect(600, 300, CARD_WIDTH, CARD_DISPLAY_HEIGHT)
                        battlefield.append(card)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= mouse_x <= 420 and 20 <= mouse_y <= 60:
                    input_active = True
                else:
                    input_active = False

                for i in range(VISIBLE_CARDS):
                    y = 80 + i * CARD_HEIGHT
                    if 20 <= mouse_x <= 420 and y <= mouse_y <= y + CARD_HEIGHT:
                        index = search_scroll + i
                        if index < len(card_objects):
                            selected_card_index = index

                for card in battlefield:
                    if card.rect.collidepoint(event.pos):
                        dragging_card = card
                        offset_x = card.rect.x - event.pos[0]
                        offset_y = card.rect.y - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_card = None

            elif event.type == pygame.MOUSEMOTION and dragging_card:
                dragging_card.rect.x = event.pos[0] + offset_x
                dragging_card.rect.y = event.pos[1] + offset_y

        draw_input_box(input_text, input_active)
        render_text("Search Results:", 20, 60)
        draw_card_list(card_objects, search_scroll, selected_card_index)

        render_text("Hand:", 300, 720)
        draw_hand(hand)

        render_text("Battlefield:", 600, 60)
        draw_table(battlefield)

        # Preview selected card
        if card_objects:
            selected_card = card_objects[selected_card_index]
            render_text("Preview:", 440, 60)
            img = get_card_image(selected_card.image_url)
            if img:
                img = pygame.transform.scale(img, (150, 210))
                screen.blit(img, (440, 90))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
