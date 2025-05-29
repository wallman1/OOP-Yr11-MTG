import pygame
import json
import os
import random
from scryfall import download_card_image, get_card_data
from Cards import Card

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MTG Game with Zones, Mana, Combat")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

ASSETS_DIR = "assets"

# Player zones
player = {
    "library": [],
    "hand": [],
    "battlefield": [],
    "graveyard": [],
    "mana_pool": {"G": 0, "R": 0, "U": 0, "B": 0, "W": 0, "C": 0},
}

def parse_mana_cost(cost):
    import re
    return re.findall(r'{(.*?)}', cost)

def can_pay_cost(cost_list, pool):
    temp_pool = pool.copy()
    for symbol in cost_list:
        if symbol.isdigit():
            generic = int(symbol)
            total_available = sum(temp_pool.values())
            if total_available < generic:
                return False
            # Subtract from any mana
            for k in temp_pool:
                while generic > 0 and temp_pool[k] > 0:
                    temp_pool[k] -= 1
                    generic -= 1
        elif symbol in temp_pool and temp_pool[symbol] > 0:
            temp_pool[symbol] -= 1
        else:
            return False
    return True

def pay_cost(cost_list, pool):
    for symbol in cost_list:
        if symbol.isdigit():
            generic = int(symbol)
            for k in pool:
                while generic > 0 and pool[k] > 0:
                    pool[k] -= 1
                    generic -= 1
        elif symbol in pool:
            pool[symbol] -= 1

def load_deck(file_path="my_deck.json"):
    if not os.path.exists(file_path):
        print("Deck file not found.")
        return []
    with open(file_path, "r") as f:
        names = json.load(f)
    deck = []
    for name in names:
        data = get_card_data(name)
        if data:
            power = int(data.get("power", 0)) if data.get("power") else 0
            toughness = int(data.get("toughness", 0)) if data.get("toughness") else 0
            mana_cost = data.get("mana_cost", "")
            image_path = download_card_image(name)
            deck.append(Card(name, power, toughness, image_path, mana_cost))
    random.shuffle(deck)
    return deck

def draw_card(player):
    if player["library"]:
        player["hand"].append(player["library"].pop(0))

def draw_card_image(card, x, y):
    card.rect.topleft = (x, y)
    try:
        img = pygame.image.load(card.image_path)
        img = pygame.transform.scale(img, (100, 140))
        screen.blit(img, (x, y))
    except:
        pygame.draw.rect(screen, (100, 0, 0), (x, y, 100, 140))
        screen.blit(font.render(card.name, True, (255, 255, 255)), (x + 5, y + 60))
    screen.blit(font.render(card.mana_cost, True, (255, 255, 0)), (x + 5, y + 5))
    screen.blit(font.render(f"{card.power}/{card.toughness}", True, (255, 255, 255)), (x + 60, y + 120))

def draw_hand(hand):
    for i, card in enumerate(hand):
        draw_card_image(card, 20 + i * 110, HEIGHT - 150)

def draw_battlefield(field):
    for i, card in enumerate(field):
        draw_card_image(card, 20 + i * 110, HEIGHT // 2 - 70)

def draw_mana_pool(pool):
    x, y = WIDTH - 150, 20
    for color, amt in pool.items():
        pygame.draw.rect(screen, (30, 30, 30), (x, y, 60, 25))
        screen.blit(font.render(f"{color}: {amt}", True, (255, 255, 255)), (x + 5, y + 5))
        y += 30

player["library"] = load_deck()
for _ in range(7):
    draw_card(player)

dragging_card = None
offset_x = offset_y = 0
phase = "main"

running = True
while running:
    screen.fill((33, 30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for card in player["hand"]:
                if card.rect.collidepoint(event.pos):
                    dragging_card = card
                    offset_x = card.rect.x - event.pos[0]
                    offset_y = card.rect.y - event.pos[1]
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_card:
                # Check if dropped in battlefield area
                if dragging_card.rect.y < HEIGHT and dragging_card.rect.y > HEIGHT // 2:
                    cost_list = parse_mana_cost(dragging_card.mana_cost)
                    if can_pay_cost(cost_list, player["mana_pool"]):
                        pay_cost(cost_list, player["mana_pool"])
                        player["hand"].remove(dragging_card)
                        player["battlefield"].append(dragging_card)
                dragging_card = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_card:
                dragging_card.rect.x = event.pos[0] + offset_x
                dragging_card.rect.y = event.pos[1] + offset_y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Simulate untapping lands to add mana
                for card in player["battlefield"]:
                    if "Forest" in card.name:
                        player["mana_pool"]["G"] += 1
            elif event.key == pygame.K_d:
                draw_card(player)

    screen.blit(font.render(f"Phase: {phase}", True, (255, 255, 255)), (20, 10))
    draw_hand(player["hand"])
    draw_battlefield(player["battlefield"])
    draw_mana_pool(player["mana_pool"])

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
