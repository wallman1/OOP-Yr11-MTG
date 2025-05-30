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
DECK_FILE = "my_deck.json"


def save_deck():
    with open(DECK_FILE, "w") as f:
        json.dump(deck, f)
    print("Deck saved.")

def load_deck():
    global deck
    if os.path.exists(DECK_FILE):
        with open(DECK_FILE, "r") as f:
            deck = json.load(f)
        print("Deck loaded.")


def search_card(name):
    global card_img
    path = download_card_image(name)
    if path:
        card_img = pygame.image.load(path)
        return True
    return False

def draw_ui():
    screen.fill((30, 30, 30))

    # Input box
    color = (0, 255, 0) if input_active else (200, 200, 200)
    pygame.draw.rect(screen, color, (20, 20, 200, 30), 2)
    text = font.render(search_text, True, (255, 255, 255))
    screen.blit(text, (25, 25))

    # Card image
    if card_img:
        screen.blit(pygame.transform.scale(card_img, (200, 280)), (20, 70))

    # Deck list
    screen.blit(font.render("Deck:", True, (255, 255, 255)), (250, 20))
    for i, name in enumerate(deck):
        screen.blit(font.render(f"{i+1}. {name}", True, (200, 200, 200)), (250, 50 + i * 25))


def main():
    global input_active, search_text
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(20, 20, 200, 30).collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False


            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if search_card(search_text):
                        deck.append(search_text)
                    search_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                else:
                    search_text += event.unicode

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if search_card(search_text):
                            deck.append(search_text)
                        search_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        search_text = search_text[:-1]
                    else:
                        search_text += event.unicode
                else:
                    if event.key == pygame.K_s:  # Press S to save
                        save_deck()
                    elif event.key == pygame.K_l:  # Press L to load
                        load_deck()


        draw_ui()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
