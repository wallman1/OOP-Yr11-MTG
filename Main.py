import pygame
import json
import os
import random
from scryfall import download_card_image, get_card_data
from Cards import Card, Creature

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MTG Game with Zones, Mana, Combat")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
global landplaced 
landplaced= False
ASSETS_DIR = "assets"

# Player zones
player = {
    "Health": 20,
    "library": [],
    "hand": [],
    "battlefield": [],
    "graveyard": [],
    "mana_pool": {"G": 0, "R": 0, "U": 0, "B": 0, "W": 0, "C": 0},
}

def parse_mana_cost(cost):
    import re
    return re.findall(r'{(.*?)}', cost)

def add_to_pool(amount, type):
    player["mana_pool"][type] += amount

def resetmana():
    player["mana_pool"]["G"] = 0
    player["mana_pool"]["R"] = 0
    player["mana_pool"]["U"] = 0
    player["mana_pool"]["B"] = 0
    player["mana_pool"]["W"] = 0
    player["mana_pool"]["C"] = 0

def tap_land(card, amount, type):
    if not card.is_tapped:
        add_to_pool(amount, type)
        card.is_tapped = True
        print(f"Tapped {card.name} for {type} mana")

def can_pay_cost(cost_list, pool):
    temp_pool = pool.copy()
    for symbol in cost_list:
        if symbol.isdigit():
            generic = int(symbol)
            total_available = sum(temp_pool.values())
            if total_available < generic:
                return False
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
            card_type = data.get("type_line")
            mana_cost = data.get("mana_cost", "")
            image_path = download_card_image(name)
            deck.append(Card(name, power, toughness, card_type, image_path, mana_cost))
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
        if card.is_tapped:
            img = pygame.transform.rotate(img, 90)
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

def untap():
    for card in player["battlefield"]:
        card.is_tapped = False
    resetmana()

def main_phase():
    pass

def draw_phase():
    draw_card(player)

phases = [untap, draw_phase, main_phase]
current_phase = 0

player["library"] = load_deck()
for _ in range(7):
    draw_card(player)

dragging_card = None
offset_x = offset_y = 0

running = True
while running:
    screen.fill((33, 30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for card in player["hand"]:
                if card.rect.collidepoint(event.pos):
                    if phases[current_phase] == main_phase:
                        if "land" in card.card_type:
                            if landplaced == False:
                                landplaced=True
                                dragging_card = card
                                offset_x = card.rect.x - event.pos[0]
                                offset_y = card.rect.y - event.pos[1]
                                pass
                            else:
                                pass
                        else:
                            dragging_card = card
                            offset_x = card.rect.x - event.pos[0]
                            offset_y = card.rect.y - event.pos[1]
                            break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for card in player["battlefield"]:
                if card.rect.collidepoint(event.pos) and not card.is_tapped:
                    name = card.name.lower()
                    if "island" in name:
                        tap_land(card, 1, "U")
                    elif "mountain" in name:
                        tap_land(card, 1, "R")
                    elif "forest" in name:
                        tap_land(card, 1, "G")
                    elif "swamp" in name:
                        tap_land(card, 1, "B")
                    elif "plains" in name:
                        tap_land(card, 1, "W")
                    else:
                        card.is_tapped = True

                    #if "Creature" in card.card_type:
                        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for card in player["battlefield"]:
                if card.rect.collidepoint(event.pos) and card.is_tapped:
                    card.is_tapped = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging_card:
                if HEIGHT // 2 < dragging_card.rect.y < HEIGHT:
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
                current_phase = (current_phase + 1) % len(phases)
                phases[current_phase]()
                if phases[current_phase] == untap:
                    landplaced = False

            elif event.key == pygame.K_d:
                draw_card(player)

            elif event.key == pygame.K_0:
                add_to_pool(1,"G")

            elif event.key == pygame.K_9:
                add_to_pool(1,"R")

            elif event.key == pygame.K_8:
                add_to_pool(1,"U")

            elif event.key == pygame.K_7:
                add_to_pool(1,"B")

            elif event.key == pygame.K_6:
                add_to_pool(1,"W")

            elif event.key == pygame.K_5:
                add_to_pool(1,"C")

            
    screen.blit(font.render(f"Player 1: {player["Health"]}", True, (255,255,255)), (20,30))
    screen.blit(font.render(f"Phase: {['Untap', 'Draw', 'Main'][current_phase]}", True, (255, 255, 255)), (20, 10))
    draw_hand(player["hand"])
    draw_battlefield(player["battlefield"])
    draw_mana_pool(player["mana_pool"])

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
