# deckbuilder.py
import pygame
import requests
from scryfall import download_card_image
import json
import os

pygame.init()
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont(None, 24)

deck = []
search_text = ""
input_active = False
card_img = None
deck_name = ""
deck_name_input_active = False
DECKS_FOLDER = "decks"

if not os.path.exists(DECKS_FOLDER):
    os.makedirs(DECKS_FOLDER)

def get_deck_path(name):
    return os.path.join(DECKS_FOLDER, f"{name}.json")

def save_deck():
    if deck_name:
        with open(get_deck_path(deck_name), "w") as f:
            json.dump(deck, f)
        print(f"Deck '{deck_name}' saved.")
    else:
        print("No deck name entered.")

def load_deck():
    global deck
    if deck_name:
        path = get_deck_path(deck_name)
        if os.path.exists(path):
            with open(path, "r") as f:
                deck = json.load(f)
            print(f"Deck '{deck_name}' loaded.")
        else:
            print(f"No saved deck found with name: {deck_name}")
    else:
        print("No deck name entered.")

def search_card(name):
    global card_img
    path = download_card_image(name)
    if path:
        card_img = pygame.image.load(path)
        return True
    return False

def draw_ui():
    screen.fill((30, 30, 30))

    # Deck name box
    name_color = (0, 255, 255) if deck_name_input_active else (180, 180, 180)
    pygame.draw.rect(screen, name_color, (20, 10, 200, 30), 2)
    name_text = font.render(deck_name or "Enter deck name", True, (255, 255, 255))
    screen.blit(name_text, (25, 15))

    # Search box
    search_color = (0, 255, 0) if input_active else (200, 200, 200)
    pygame.draw.rect(screen, search_color, (20, 50, 200, 30), 2)
    search_surface = font.render(search_text, True, (255, 255, 255))
    screen.blit(search_surface, (25, 55))

    # Card image
    if card_img:
        screen.blit(pygame.transform.scale(card_img, (200, 280)), (20, 100))

    # Deck list
    screen.blit(font.render(f"Deck: {deck_name or 'Unnamed'}", True, (255, 255, 255)), (250, 10))
    for i, name in enumerate(deck):
        screen.blit(font.render(f"{i+1}. {name}", True, (200, 200, 200)), (250, 40 + i * 25))

    # Instructions
    screen.blit(font.render("Type card name and press Enter to add", True, (150, 150, 150)), (20, 400))
    screen.blit(font.render("S = Save deck | L = Load deck", True, (150, 150, 150)), (20, 420))

def main():
    global input_active, search_text, deck_name, deck_name_input_active
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(20, 10, 200, 30).collidepoint(event.pos):
                    deck_name_input_active = True
                    input_active = False
                elif pygame.Rect(20, 50, 200, 30).collidepoint(event.pos):
                    input_active = True
                    deck_name_input_active = False
                else:
                    input_active = False
                    deck_name_input_active = False

            elif event.type == pygame.KEYDOWN:
                if deck_name_input_active:
                    if event.key == pygame.K_RETURN:
                        deck_name_input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        deck_name = deck_name[:-1]
                    else:
                        deck_name += event.unicode

                elif input_active:
                    if event.key == pygame.K_RETURN:
                        if search_card(search_text):
                            deck.append(search_text)
                        search_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        search_text = search_text[:-1]
                    else:
                        search_text += event.unicode

                else:
                    if event.key == pygame.K_s:
                        save_deck()
                    elif event.key == pygame.K_l:
                        load_deck()

        draw_ui()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
