import pygame
import json
import os
import random
from scryfall import download_card_image, get_card_data
from Cards import Card, Creature, Artifact, Planeswalker

pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("MTG Game with Zones, Mana, Combat")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
global landplaced 
landplaced = False
ASSETS_DIR = "assets"
pending_triggers = []

# Players
players = [
    {
        "Health": 20,
        "library": "my_deck.json",
        "hand": [],
        "battlefield": [],
        "graveyard": [],
        "mana_pool": {"G": 0, "R": 0, "U": 0, "B": 0, "W": 0, "C": 0},
        "deck": "deck2.json"
    },
    {
        "Health": 20,
        "library": [],
        "hand": [],
        "battlefield": [],
        "graveyard": [],
        "mana_pool": {"G": 0, "R": 0, "U": 0, "B": 0, "W": 0, "C": 0},
        "deck": "my_deck.json"
    }
]
current_player = 0
attackers = []
blockers = {}
selecting_attackers = False
selecting_blockers = False
combat_animations = []

stack = []

combat_keywords = {
    "first strike": "first_strike",
    "trample": "trample",
}

def parse_mana_cost(cost):
    import re
    return re.findall(r'{(.*?)}', cost)

def add_to_pool(player, amount, type):
    player["mana_pool"][type] += amount

def resetmana(player):
    for color in player["mana_pool"]:
        player["mana_pool"][color] = 0

def tap_land(player, card, amount, type):
    if not card.is_tapped:
        add_to_pool(player, amount, type)
        card.is_tapped = True
        print(f"Tapped {card.name} for {type} mana")

def addlife(player, amount):
    player["Health"] += amount

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

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def load_deck(card_list):
    deck = []
    if not os.path.exists(card_list):
        print("Deck file not found.")
        return []
    with open(card_list, "r") as f:
        names = json.load(f)
    for name in names:
        card_data = get_card_data(name)
        power = safe_int(card_data.get("power", 0))
        toughness = safe_int(card_data.get("toughness", 0))
        card_type = card_data["type_line"]
        mana_cost = card_data.get("mana_cost", "")
        image_path = download_card_image(name)
        print(image_path)
        print(name)  # or however you store image_path
        #if "Planeswalker" in card_type:
            #loyalty = card_data["loyalty"]
            #print(loyalty)
            #abilities = card_data.get("oracle_text", "").split("\n")  # just a placeholder
            #deck.append(Planeswalker(name, power, toughness, mana_cost, loyalty, abilities, image_path))
        if "Artifact" in card_type:
            deck.append(Artifact(name, mana_cost, image_path))
        else:
            print(name)
            deck.append(Card(name, power, toughness, card_type, image_path, mana_cost))

    random.shuffle(deck)
    return deck

def parse_planeswalker_abilities(data):
    # This function should parse the abilities from the card data
    # For simplicity, we'll return an empty list here
    return []

def handle_enter_the_battlefield(card, player):
    if "gain life" in card.oracle_text.lower():
        import re
        match = re.search(r"gain (\d+) life", card.oracle_text.lower())
        if match:
            amount = int(match.group(1))
            addlife(player, amount)
            print(f"{card.name} triggered: Gained {amount} life.")


def draw_card(player):
    if player["library"]:
        player["hand"].append(player["library"].pop(0))

def draw_card_image(card, x, y):
    card.rect.topleft = (x, y)
    img = None
    print(card.name)
    if os.path.exists(card.image_path):
        try:
            img = pygame.image.load(card.image_path)
            img = pygame.transform.scale(img, (100, 140))
            if card.is_tapped:
                img = pygame.transform.rotate(img, 90)
            screen.blit(img, (x, y))
        except pygame.error as e:
            print(f"Failed to load image {card.image_path}: {e}")
    else:
        print(f"Image path does not exist: {card.image_path}")
    #if img is None:
        #pygame.draw.rect(screen, (100, 0, 0), (x, y, 100, 140))
        #print("name",card.image_path)
        #screen.blit(font.render(card.name, True, (255, 255, 255)), (x + 5, y + 60))
    #screen.blit(font.render(card.mana_cost, True, (255, 255, 0)), (x + 5, y + 5))
    if isinstance(card, Creature):
        screen.blit(font.render(f"{card.power}/{card.toughness}", True, (255, 255, 255)), (x + 60, y + 120))
    elif isinstance(card, Planeswalker):
        screen.blit(font.render(f"Loyalty: {card.loyalty}", True, (255, 255, 255)), (x + 5, y + 120))



def draw_hand(hand, y_offset, is_current_player):
    for i, card in enumerate(hand):
        x = 20 + i * 110
        if is_current_player:
            pygame.draw.rect(screen, (255, 255, 0), (x - 5, y_offset - 5, 110, 150), 3)
        draw_card_image(card, x, y_offset)

def draw_battlefield(field, offset_y):
    for i, card in enumerate(field):
        draw_card_image(card, 20 + i * 110, offset_y)

def draw_mana_pool(pool, x, y):
    for color, amt in pool.items():
        pygame.draw.rect(screen, (30, 30, 30), (x, y, 60, 25))
        screen.blit(font.render(f"{color}: {amt}", True, (255, 255, 255)), (x + 5, y + 5))
        y += 30

def resolve_combat_stack():
    while stack:
        effect = stack.pop()
        effect()

def handle_combat_animations():
    for atk, blk in combat_animations:
        pygame.draw.line(screen, (255, 0, 0), atk.rect.center, blk.rect.center, 4)

def combat_phase():
    global selecting_attackers, attackers, blockers, combat_animations
    selecting_attackers = True
    attackers = []
    blockers = {}
    combat_animations = []

def combat_resolution_phase():
    global attackers, blockers, combat_animations
    resolve_combat_stack()
    for attacker in attackers:
        blocker = blockers.get(attacker)
        if blocker:
            combat_animations.append((attacker, blocker))
            atk_dmg = attacker.power
            blk_dmg = blocker.power

            if "first strike" in attacker.name.lower():
                blocker.toughness -= atk_dmg
                if blocker.toughness <= 0:
                    players[1 - current_player]["battlefield"].remove(blocker)
                    players[1 - current_player]["graveyard"].append(blocker)
                else:
                    attacker.toughness -= blk_dmg
            else:
                attacker.toughness -= blk_dmg
                blocker.toughness -= atk_dmg

            if not blocker:
                damage = attacker.power
                players[1 - current_player]["Health"] -= damage
                if "lifelink" in attacker.oracle_text.lower():
                    players[current_player]["Health"] += damage
                    print(f"{attacker.name} lifelink: Gained {damage} life.")

            if attacker.toughness <= 0:
                players[current_player]["battlefield"].remove(attacker)
                players[current_player]["graveyard"].append(attacker)
            if blocker.toughness <= 0 and blocker in players[1 - current_player]["battlefield"]:
                players[1 - current_player]["battlefield"].remove(blocker)
                players[1 - current_player]["graveyard"].append(blocker)
        else:
            target = attacker.target  # Assume this attribute is set during attacker selection
            if isinstance(target, Planeswalker):
                target.loyalty -= attacker.power
                if target.loyalty <= 0:
                    players[1 - current_player]["battlefield"].remove(target)
                    players[1 - current_player]["graveyard"].append(target)
            else:
                players[1 - current_player]["Health"] -= attacker.power

    attackers = []
    blockers = []
    combat_animations = []

def trigger_card_effect(card, controller):
    text = card.oracle_text.lower()

    # === One-time effects ===
    if "draw a card" in text:
        draw_card(controller)

    # === Buffs ===
    import re
    match = re.search(r'gets \+(\d+)/\+(\d+)', text)
    if match:
        card.power += int(match.group(1))
        card.toughness += int(match.group(2))

    # === Damage effects ===
    match = re.search(r'deals (\d+) damage to any target', text)
    if match:
        damage = int(match.group(1))
        # Simplified: deal to opponent
        players[1 - current_player]["Health"] -= damage
        print(f"{card.name} deals {damage} damage to opponent")

    # === Mana abilities ===
    if "tap:" in text and "add {" in text:
        color_match = re.search(r'add {([gubrw])}', text)
        if color_match:
            color = color_match.group(1).upper()
            def ability():
                tap_land(controller, card, 1, color)
            card.activated_ability = ability
            print(f"{card.name} gains ability: tap to add {color} mana")

    # === Keyword abilities ===
    if "flying" in text:
        card.keywords.append("flying")
    if "trample" in text:
        card.keywords.append("trample")
    if "first strike" in text:
        card.keywords.append("first strike")

def handle_triggers(phase):
    for card in players[current_player]["battlefield"]:
        if "at the beginning of your upkeep" in card.oracle_text.lower() and phase == "upkeep":
            pending_triggers.append(lambda: draw_card(players[current_player]))

def activate_planeswalker_ability(player, planeswalker, ability_index):
    if planeswalker.has_activated_ability:
        print("This planeswalker has already activated an ability this turn.")
        return
    if 0 <= ability_index < len(planeswalker.abilities):
        ability = planeswalker.abilities[ability_index]
        cost = ability['cost']
        effect = ability['effect']
        new_loyalty = planeswalker.loyalty + cost
        if new_loyalty < 0:
            print("Not enough loyalty to activate this ability.")
            return
        planeswalker.loyalty = new_loyalty
        effect()
        planeswalker.has_activated_ability = True
    else:
        print("Invalid ability index.")

def activate_artifact(player, artifact):
    # Define the effect of the artifact
    pass

def untap():
    resetmana(players[current_player])
    for card in players[current_player]["battlefield"]:
        card.is_tapped = False
        if isinstance(card, Planeswalker):
            card.has_activated_ability = False

def draw_phase():
    draw_card(players[current_player])

def main_phase():
    pass

phases = [untap, draw_phase, main_phase, combat_phase, combat_resolution_phase]
current_phase = 0

for p in players:
    p["library"] = load_deck(p["deck"])
    for _ in range(7):
        draw_card(p)

dragging_card = None
offset_x = offset_y = 0

running = True
while running:
    screen.fill((33, 30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if selecting_attackers:
                for card in players[current_player]["battlefield"]:
                    if card.rect.collidepoint(event.pos) and not card.is_tapped and isinstance(card, Creature):
                        card.is_tapped = True
                        attackers.append(card)
                selecting_attackers = False
                selecting_blockers = True

            elif selecting_blockers:
                for card in players[1 - current_player]["battlefield"]:
                    if card.rect.collidepoint(event.pos) and not card.is_tapped and isinstance(card, Creature):
                        for atk in attackers:
                            if atk not in blockers:
                                blockers[atk] = card
                                card.is_tapped = True
                                break
                selecting_blockers = False

            else:
                for card in players[current_player]["hand"]:
                    print("name",card)
                    if card.rect.collidepoint(event.pos):
                        if phases[current_phase] == main_phase:
                            if "land" in card.card_type:
                                if not landplaced:
                                    landplaced = True
                                    players[current_player]["battlefield"].append(dragging_card)
                                    trigger_card_effect(dragging_card, players[current_player])
                                    dragging_card = card
                                    offset_x = card.rect.x - event.pos[0]
                                    offset_y = card.rect.y - event.pos[1]
                            else:
                                players[current_player]["battlefield"].append(dragging_card)
                                trigger_card_effect(dragging_card, players[current_player])
                                dragging_card = card
                                offset_x = card.rect.x - event.pos[0]
                                offset_y = card.rect.y - event.pos[1]
                            break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for card in players[current_player]["battlefield"]:
                if card.rect.collidepoint(event.pos) and not card.is_tapped:
                    name = card.name.lower()
                    if "Land" in card.card_type:
                        tap_land(players[current_player], card, 1, "G" if "forest" in name else
                                                                    "U" if "island" in name else
                                                                    "R" if "mountain" in name else
                                                                    "B" if "swamp" in name else
                                                                    "W" if "plains" in name else "C")
                    elif "Creature" in card.card_type:
                        card.is_tapped = True

                    elif isinstance(card, Artifact):
                        activate_artifact(players[current_player], card)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for card in players[current_player]["battlefield"]:
                if card.rect.collidepoint(event.pos) and card.is_tapped:
                    card.is_tapped = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging_card:
                if (current_player == 0 and HEIGHT // 2 < dragging_card.rect.y < HEIGHT) or \
                (current_player == 1 and 0 < dragging_card.rect.y < HEIGHT // 2):
                    cost_list = parse_mana_cost(dragging_card.mana_cost)
                    if can_pay_cost(cost_list, players[current_player]["mana_pool"]):
                        pay_cost(cost_list, players[current_player]["mana_pool"])
                        players[current_player]["hand"].remove(dragging_card)
                        players[current_player]["battlefield"].append(dragging_card)
                dragging_card = None

            if HEIGHT // 2 < dragging_card.rect.y < HEIGHT:
                cost_list = parse_mana_cost(dragging_card.mana_cost)
                if can_pay_cost(cost_list, players[current_player]["mana_pool"]):
                    pay_cost(cost_list, players[current_player]["mana_pool"])
                    players[current_player]["hand"].remove(dragging_card)
                    players[current_player]["battlefield"].append(dragging_card)
                    handle_enter_the_battlefield(dragging_card, players[current_player])


        elif event.type == pygame.MOUSEMOTION:
            if dragging_card:
                dragging_card.rect.x = event.pos[0] + offset_x
                dragging_card.rect.y = event.pos[1] + offset_y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_phase = (current_phase + 1) % len(phases)
                phases[current_phase]()
                if phases[current_phase] == combat_resolution_phase:
                    if current_player < 1:
                        current_player += 1
                    else:
                        current_player = 0
                if phases[current_phase] == untap:
                    landplaced = False

            elif event.key == pygame.K_d:
                draw_card(players[current_player])

            if event.key == pygame.K_SPACE:
                current_player = current_player
                landplaced = False
                resetmana(players[current_player])
                for card in players[current_player]["battlefield"]:
                    card.is_tapped = False
                print(f"Player {current_player + 1}'s turn")

            # Play card from hand
            elif event.key in [pygame.K_e, pygame.K_RETURN]:
                player = players[current_player]
                hand = player["hand"]
                if hand:
                    selected = hand[0]  # Simplified: auto-select first card
                    if "Land" in selected.card_type:
                        if not landplaced:
                            landplaced = True
                            player["battlefield"].append(selected)
                            player["hand"].remove(selected)
                    else:
                        cost = parse_mana_cost(selected.mana_cost)
                        if can_pay_cost(cost, player["mana_pool"]):
                            pay_cost(cost, player["mana_pool"])
                            player["battlefield"].append(selected)
                            player["hand"].remove(selected)
                            handle_enter_the_battlefield(selected, player) 

            # Tap first untapped land
            elif event.key in [pygame.K_t]:
                player = players[current_player]
                for card in player["battlefield"]:
                    if "Land" in card.card_type and not card.is_tapped:
                        name = card.name.lower()
                        tap_land(player, card, 1, "G" if "forest" in name else
                                                 "U" if "island" in name else
                                                 "R" if "mountain" in name else
                                                 "B" if "swamp" in name else
                                                 "W" if "plains" in name else "C")
                        
            elif event.key in [pygame.K_0]:
                player = players[current_player]
                add_to_pool(player, 1, "G")

            elif event.key in [pygame.K_9]:
                player = players[current_player]
                add_to_pool(player, 1, "R")

            elif event.key in [pygame.K_8]:
                player = players[current_player]
                add_to_pool(player, 1, "U")

            elif event.key in [pygame.K_7]:
                player = players[current_player]
                add_to_pool(player, 1, "B")

            elif event.key in [pygame.K_6]:
                player = players[current_player]
                add_to_pool(player, 1, "W")

            elif event.key in [pygame.K_5]:
                player = players[current_player]
                add_to_pool(player, 1, "C")

            elif event.key in [pygame.K_l]:
                player = players[current_player]
                addlife(player,1)

            elif event.key in [pygame.K_j]:
                player = players[current_player]
                addlife(player,-1)
    if players[current_player]["Health"] <= 0:
        screen.blit(font.render(f"Player {current_player+1} has died", True, (255,255,255)),(500,500))


    screen.blit(font.render(f"Player 1: {players[0]['Health']}", True, (255,255,255)), (20,10))
    screen.blit(font.render(f"Player 2: {players[1]['Health']}", True, (255,255,255)), (20, HEIGHT - 180))
    screen.blit(font.render(f"Current Turn: Player {current_player + 1}", True, (255,255,255)), (WIDTH // 2 - 100, 10))
    screen.blit(font.render(f"Phase: {['Untap', 'Draw', 'Main', 'Combat', 'Resolution'][current_phase]}", True, (255,255,255)), (WIDTH // 2 - 100, 40))

    draw_hand(players[0]["hand"], HEIGHT - 150, current_player == 0)
    draw_hand(players[1]["hand"], 50, current_player == 1)
    draw_battlefield(players[0]["battlefield"], HEIGHT // 2 + 80)
    draw_battlefield(players[1]["battlefield"], HEIGHT // 2 - 220)
    draw_mana_pool(players[0]["mana_pool"], WIDTH - 150, HEIGHT - 200)
    draw_mana_pool(players[1]["mana_pool"], WIDTH - 150, 80)

    handle_combat_animations()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
