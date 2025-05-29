# TopDecked-like Pygame Application
# Features:
# - Card search bar
# - Card image preview
# - Add to deck with mouse click
# - Remove from deck with click
# - Deck list with counts
# - Scrollable search results and deck list
# - Cached card image loading for performance

import pygame
import requests
from scryfall_api import search_cards
from Cards import Card
from Deck import Deck
from io import BytesIO

pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("TopDecked Clone")
font = pygame.font.SysFont("Arial", 20)
input_font = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BG_COLOR = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)

CARD_HEIGHT = 40
VISIBLE_CARDS = 15
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

def draw_deck_list(deck_cards, start_index):
    counts = {}
    for card in deck_cards:
        counts[card.name] = counts.get(card.name, 0) + 1
    unique_cards = list(counts.items())
    for i, (name, count) in enumerate(unique_cards[start_index:start_index + VISIBLE_CARDS]):
        y = 80 + i * CARD_HEIGHT
        pygame.draw.rect(screen, LIGHT_GRAY, (860, y, 400, CARD_HEIGHT), 0)
        render_text(f"{count}x {name}", 865, y + 10)

def main():
    running = True
    clock = pygame.time.Clock()

    input_text = ""
    input_active = False

    deck = Deck()
    selected_card_index = 0
    search_scroll = 0
    deck_scroll = 0

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
                    if event.key == pygame.K_DOWN:
                        selected_card_index = min(selected_card_index + 1, len(card_objects) - 1)
                        if selected_card_index - search_scroll >= VISIBLE_CARDS:
                            search_scroll += 1
                    elif event.key == pygame.K_UP:
                        selected_card_index = max(selected_card_index - 1, 0)
                        if selected_card_index < search_scroll:
                            search_scroll = max(search_scroll - 1, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= mouse_x <= 420 and 20 <= mouse_y <= 60:
                    input_active = True
                else:
                    input_active = False

                # Check if clicked on card list
                for i in range(VISIBLE_CARDS):
                    y = 80 + i * CARD_HEIGHT
                    if 20 <= mouse_x <= 420 and y <= mouse_y <= y + CARD_HEIGHT:
                        index = search_scroll + i
                        if index < len(card_objects):
                            deck.add_card(card_objects[index])

                # Check if clicked on deck list
                for i in range(VISIBLE_CARDS):
                    y = 80 + i * CARD_HEIGHT
                    if 860 <= mouse_x <= 1260 and y <= mouse_y <= y + CARD_HEIGHT:
                        index = deck_scroll + i
                        if index < len(deck.cards):
                            deck.remove_card(deck.cards[index].name)

        draw_input_box(input_text, input_active)
        render_text("Search Results:", 20, 60)
        render_text("Deck:", 860, 60)
        draw_card_list(card_objects, search_scroll, selected_card_index)
        draw_deck_list(deck.cards, deck_scroll)

        # Show selected card preview
        if card_objects:
            selected_card = card_objects[selected_card_index]
            render_text("Preview:", 460, 60)
            img = get_card_image(selected_card.image_url)
            if img:
                img = pygame.transform.scale(img, (300, 420))
                screen.blit(img, (460, 90))
            else:
                render_text("Image failed to load", 460, 90)

        pygame.display.flip()
        clock.tick(60)

    deck.save()

if __name__ == "__main__":
    main()
