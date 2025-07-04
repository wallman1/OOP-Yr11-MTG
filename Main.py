import pygame
import json
import os
import random
import re
from scryfall import download_card_image, get_card_data
from Cards import Card, Creature, Artifact, Planeswalker

pygame.init()
# Initialize display
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("MTG Game with Zones, Mana, Combat")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
# UI Elements
search_button = pygame.Rect(WIDTH - 220, HEIGHT // 2 - 25, 200, 40)
# Game state variables
landplaced = False
ASSETS_DIR = "assets"
pending_triggers = []
selected_planeswalker = None
ability_buttons = []  # List of tuples (Rect, ability_text)
searching_card = False
input_text = ""
search_result_message = ""


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
# Define common keywords with their effects as lambdas
KEYWORDS = {
    "flying": lambda card: setattr(card, "has_flying", True),
    "trample": lambda card: setattr(card, "has_trample", True),
    "deathtouch": lambda card: setattr(card, "has_deathtouch", True),
    "lifelink": lambda card: setattr(card, "has_lifelink", True),
}
# Conditions for effects
CONDITIONS = {
    "if you control a creature": lambda player, opp: any(isinstance(c, Creature) for c in player["battlefield"]),
    "if opponent has more life": lambda player, opp: opp["Health"] > player["Health"],
    # Add more conditions as needed
}
current_player = 0
attackers = []
blockers = {}
selecting_attackers = False
selecting_blockers = False
combat_animations = []

stack = []
# Keywords relevant during combat
combat_keywords = {
    "first strike": "first_strike",
    "trample": "trample",
}

def parse_mana_cost(cost):
    """
    Parses a mana cost string and returns a list of individual mana symbols.

    Args:
        cost (str): The mana cost string, e.g., "{G}{U}{2}".

    Returns:
        list: A list of mana symbols extracted from the string.
    """
    import re
    return re.findall(r'{(.*?)}', cost)

def add_to_pool(player, amount, type):
    """
    Adds a specified amount of mana of a given type to a player's mana pool.

    Args:
        player (dict): The player dictionary containing 'mana_pool'.
        amount (int): The amount of mana to add.
        type (str): The mana type (e.g., "G", "U").
    """
    player["mana_pool"][type] += amount

def resetmana(player):
    """
    Resets all mana in a player's mana pool to zero.

    Args:
        player (dict): The player dictionary with 'mana_pool'.
    """
    for color in player["mana_pool"]:
        player["mana_pool"][color] = 0

def tap_land(player, card, amount, type):
    """
    Taps a land card and adds mana to the player's mana pool.

    Args:
        player (dict): The player performing the action.
        card (Card): The land card to tap.
        amount (int): The amount of mana to produce.
        type (str): The mana color/type (e.g., "G", "U").
    """
    if not card.is_tapped:
        add_to_pool(player, amount, type)
        card.is_tapped = True
        print(f"Tapped {card.name} for {type} mana")

def addlife(player, amount):
    """
    Adds life points to a player.

    Args:
        player (dict): The player to add life to.
        amount (int): The amount of life to add (can be negative).
    """
    player["Health"] += amount

def can_pay_cost(cost_list, pool):
    """
    Checks if the current mana pool can pay the specified mana cost.

    Args:
        cost_list (list): List of mana symbols required.
        pool (dict): The current mana pool with keys as mana types and values as amounts.

    Returns:
        bool: True if the pool can pay the cost, False otherwise.
    """
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
    """
    Deducts mana cost from the player's mana pool.

    Args:
        cost_list (list): List of mana symbols required.
        pool (dict): The player's mana pool to modify.
    """
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
    """
    Safely converts a value to an integer, returns 0 if conversion fails.

    Args:
        value: The value to convert.

    Returns:
        int: The integer value or 0 if conversion fails.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def load_deck(card_list):
    """
    Loads a deck from a JSON file, retrieves card data, creates card objects, and returns a shuffled deck.

    Args:
        card_list (str): Path to the JSON file containing list of card names.

    Returns:
        list: List of card objects (Creature, Artifact, Card, etc.) shuffled randomly.
    """
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
        oracle_text = card_data.get("oracle_text")# or however you store image_path
        if "Planeswalker" in card_type:
            loyalty = int(card_data.get("loyalty", 0))  # Ensure loyalty is an integer
            abilities = card_data.get("oracle_text", "").split("\n")
            deck.append(Planeswalker(name, mana_cost, image_path, loyalty, abilities))

        elif "Artifact" in card_type:
            deck.append(Artifact(name, image_path, mana_cost, oracle_text))
        elif "Creature" in card_type:
            deck.append(Creature(name, image_path, mana_cost, power, toughness, oracle_text))
        else:
            deck.append(Card(name, card_type, image_path, mana_cost, oracle_text))

    random.shuffle(deck)
    return deck

def apply_planeswalker_ability(card, ability_text, player):
    """
    Applies the effect of a planeswalker ability.

    Args:
        card (Planeswalker): The planeswalker card activating the ability.
        ability_text (str): The text describing the ability.
        player (dict): The player who controls the planeswalker.
    """
    import re
    match = re.match(r"([+-]?\d+):\s*(.*)", ability_text)
    if match:
        loyalty_change = int(match.group(1))
        effect = match.group(2).strip().lower()
        card.loyalty += loyalty_change
        card.has_activated_ability = True

        # Effect Handling
        if "draw a card" in effect:
            draw_card(player)

        elif "gain life" in effect:
            gain_match = re.search(r"gain (\d+) life", effect)
            if gain_match:
                amount = int(gain_match.group(1))
                addlife(player, amount)

        elif "deal" in effect and "damage" in effect:
            dmg_match = re.search(r"deal (\d+) damage", effect)
            if dmg_match:
                dmg = int(dmg_match.group(1))
                players[1 - current_player]["Health"] -= dmg
                print(f"{card.name} deals {dmg} damage to opponent")

        # Add more effects as needed
    else:
        print("Invalid planeswalker ability format.")

def choose_planeswalker_ability(card, player):
    """
    Prompts user to select a planeswalker ability to activate.

    Args:
        card (Planeswalker): The planeswalker card.
        player (dict): The player controlling the planeswalker.
    """
    print(f"Choose an ability for {card.name}:")
    for idx, ability in enumerate(card.abilities):
        print(f"{idx + 1}: {ability}")
    
    try:
        choice = int(input("Enter ability number: ")) - 1
        if 0 <= choice < len(card.abilities):
            apply_planeswalker_ability(card, card.abilities[choice], player)
            card.has_activated_ability = True
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")



def draw_card(player):
    """
    Draws a card from the player's library into their hand.

    Args:
        player (dict): The player drawing the card.
    """
    if player["library"]:
        new_card = player["library"].pop()
        player["hand"].append(new_card)
        current_index = players.index(player)
        check_triggered_effects("you draw a card", current_index, 1 - current_index)


def discard_card(player):
    """
    Discards a card from the player's hand into their graveyard.

    Args:
        player (dict): The player discarding the card.
    """
    if player["hand"]:
        player["graveyard"].append(player["hand"].pop(0))

def buff_creature(card,a,b):
    """
    Buffs a creature's power and toughness.

    Args:
        card (Card): The creature card to buff.
        a (int): The amount to add to toughness.
        b (int): The amount to add to power.
    """
    try:
        card.power += int(b)
        card.toughness += int(a)
    except:
        print("card not creature")

def draw_card_image(card, x=None, y=None):
    """
    Draws the visual representation of a card, including image and stats overlays.

    Args:
        card (Card): The card object to draw.
        x (int, optional): The x-coordinate for position. Defaults to None.
        y (int, optional): The y-coordinate for position. Defaults to None.
    """
    img = None

    if x is not None and y is not None:
        card.rect.topleft = (x, y)  # Only set position if explicitly passed
    elif not card.rect.topleft:
        card.rect.topleft = (0, 0)  # Ensure it's not uninitialized

    if os.path.exists(card.image_path):
        try:
            img = pygame.image.load(card.image_path)
            img = pygame.transform.scale(img, (100, 140))
            if card.is_tapped:
                img = pygame.transform.rotate(img, 90)
            screen.blit(img, card.rect.topleft)
        except pygame.error as e:
            print(f"Failed to load image {card.image_path}: {e}")
    else:
        print(f"Image path does not exist: {card.image_path}")

    # Overlay info
    mana_text = str(card.mana_cost) if card.mana_cost else ""
    screen.blit(font.render(mana_text, True, (255, 255, 0)), (card.rect.left + 5, card.rect.top + 5))
    
    if isinstance(card, Creature):
        screen.blit(font.render(f"{card.power}/{card.toughness}", True, (255, 255, 255)), (card.rect.left + 60, card.rect.top + 120))
    elif isinstance(card, Planeswalker):
        screen.blit(font.render(f"Loyalty: {card.loyalty}", True, (255, 0, 0)), (card.rect.left + 5, card.rect.top + 120))




def draw_hand(hand, y_offset, is_current_player):
    """
    Draws the player's hand cards at a specific y position.

    Args:
        hand (list): List of card objects in player's hand.
        y_offset (int): Y position offset for drawing.
        is_current_player (bool): Whether this hand belongs to current player (for highlighting).
    """
    for i, card in enumerate(hand):
        x = 20 + i * 110
        if is_current_player:
            pygame.draw.rect(screen, (255, 255, 0), (x - 5, y_offset - 5, 110, 150), 3)
        draw_card_image(card, x, y_offset)

def draw_battlefield(field, offset_y):
    """
    Draws cards on the battlefield.

    Args:
        field (list): List of card objects on the battlefield.
        offset_y (int): Y position offset.
    """
    for i, card in enumerate(field):
        draw_card_image(card, 20 + i * 110, offset_y)

def draw_mana_pool(pool, x, y):
    """
    Draws the player's mana pool.

    Args:
        pool (dict): Dictionary with mana types as keys and amounts as values.
        x (int): X coordinate for starting position.
        y (int): Y coordinate for starting position.
    """
    for color, amt in pool.items():
        pygame.draw.rect(screen, (30, 30, 30), (x, y, 60, 25))
        screen.blit(font.render(f"{color}: {amt}", True, (255, 255, 255)), (x + 5, y + 5))
        y += 30

def resolve_combat_stack():
    """
    Resolves all effects in the stack during combat.
    """
    while stack:
        effect = stack.pop()
        effect()

def handle_combat_animations():
    """
    Draws lines representing combat damage animations.
    """
    for atk, blk in combat_animations:
        pygame.draw.line(screen, (255, 0, 0), atk.rect.center, blk.rect.center, 4)

def combat_phase():
    """
    Starts the combat phase, enabling attacker and blocker selection.
    """
    global selecting_attackers, attackers, blockers, combat_animations
    selecting_attackers = True
    attackers = []
    blockers = {}
    combat_animations = []

def combat_resolution_phase():
    """
    Resolves combat damage, creature deaths, and effects after combat.
    """
    global attackers, blockers, combat_animations
    resolve_combat_stack()

    for attacker in attackers:
        blocker = blockers.get(attacker)
        damage_to_opponent = 0

        if blocker:
            combat_animations.append((attacker, blocker))

            atk_power = attacker.power
            blk_power = blocker.power

            atk_keywords = getattr(attacker, 'keywords', set())
            blk_keywords = getattr(blocker, 'keywords', set())

            # First Strike / Double Strike resolution step 1
            if "first strike" in atk_keywords or "double strike" in atk_keywords:
                blocker.toughness -= atk_power
                if "deathtouch" in atk_keywords:
                    blocker.toughness = 0
                if blocker.toughness <= 0:
                    players[1 - current_player]["battlefield"].remove(blocker)
                    players[1 - current_player]["graveyard"].append(blocker)
                else:
                    attacker.toughness -= blk_power
                if "deathtouch" in blk_keywords:
                    attacker.toughness = 0
            else:
                # Normal damage exchange
                attacker.toughness -= blk_power
                blocker.toughness -= atk_power
                if "deathtouch" in atk_keywords:
                    blocker.toughness = 0
                if "deathtouch" in blk_keywords:
                    attacker.toughness = 0

            # Remove dead creatures
            if attacker.toughness <= 0:
                players[current_player]["battlefield"].remove(attacker)
                players[current_player]["graveyard"].append(attacker)

            if blocker.toughness <= 0 and blocker in players[1 - current_player]["battlefield"]:
                players[1 - current_player]["battlefield"].remove(blocker)
                players[1 - current_player]["graveyard"].append(blocker)

            # Double Strike second step (if blocker survived)
            if "double strike" in atk_keywords and blocker in players[1 - current_player]["battlefield"]:
                blocker.toughness -= atk_power
                if "deathtouch" in atk_keywords:
                    blocker.toughness = 0
                if blocker.toughness <= 0:
                    players[1 - current_player]["battlefield"].remove(blocker)
                    players[1 - current_player]["graveyard"].append(blocker)

        else:
            # No blocker - damage goes to player or planeswalker
            target = getattr(attacker, 'target', None)
            damage = attacker.power
            atk_keywords = getattr(attacker, 'keywords', set())

            if "trample" in atk_keywords and attacker in blockers:
                # Excess damage to player (if partial block logic is implemented later)
                damage_to_opponent = attacker.power  # Full for now
            else:
                damage_to_opponent = attacker.power

            if isinstance(target, Planeswalker):
                target.loyalty -= damage_to_opponent
                if target.loyalty <= 0:
                    players[1 - current_player]["battlefield"].remove(target)
                    players[1 - current_player]["graveyard"].append(target)
            else:
                players[1 - current_player]["Health"] -= damage_to_opponent

            if "lifelink" in atk_keywords:
                players[current_player]["Health"] += damage_to_opponent
                print(f"{attacker.name} lifelink: Gained {damage_to_opponent} life.")

    attackers.clear()
    blockers.clear()
    combat_animations.clear()

def parse_effect(text):
    """
    Parses a spell or ability text into a list of effect dictionaries.

    Args:
        text (str): The textual description of effects.

    Returns:
        list: List of effect dictionaries with 'type' and other keys.
    """
    print(text)
    effects = []
    lines = text.lower().split(".")
    print(lines)
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # --- Triggered Effects ---
        trigger_match = re.match(r'(when|whenever|at) (.+?), (.+)', line)
        if trigger_match:
            trigger_type = trigger_match.group(1)
            trigger_condition = trigger_match.group(2).strip()
            trigger_action = trigger_match.group(3).strip()
            
            effects.append({
                "type": "trigger",
                "trigger": trigger_condition,
                "effects": parse_effect(trigger_action)  # recurse on action
            })
            continue


        # --- Conditionals ---
        for condition_text, condition_func in CONDITIONS.items():
            if condition_text in line:
                print("match")
                after_then = line.split(condition_text)[-1].replace("then ", "").strip()
                sub_effects = parse_effect(after_then)
                effects.append({
                    "type": "conditional",
                    "condition": condition_func,
                    "effects": sub_effects
                })
                break
        else:
            # --- Keywords ---
            for keyword, action in KEYWORDS.items():
                if keyword in line:
                    print("match")
                    effects.append({
                        "type": "keyword",
                        "keyword": keyword,
                        "action": action
                    })
                    break

            # --- Buffs (e.g., +1/+1) ---
            buff_match = re.search(r'\+(\d+)/\+(\d+)', line)
            if buff_match:
                print("match")
                p, t = map(int, buff_match.groups())
                effects.append({
                    "type": "buff",
                    "power": p,
                    "toughness": t
                })
                continue

            # --- Draw Cards ---
            if "draw" in line and "card" in line:
                print("match")
                draw_count = 1
                count_match = re.search(r'draw (\d+)', line)
                if count_match:
                    draw_count = int(count_match.group(1))
                effects.append({
                    "type": "draw",
                    "amount": draw_count
                })

            # --- Damage to Player ---
            dmg_match = re.search(r'deal (\d+) damage to target player', line)
            if dmg_match:
                print("match")
                damage = int(dmg_match.group(1))
                effects.append({
                    "type": "damage",
                    "target": "player",
                    "amount": damage
                })
    print(effects)
    return effects



def apply_effect(effect, source_card, controller_index):
    """
    Applies a specific effect to the game state.

    Args:
        effect (dict): The effect dictionary to apply.
        source_card (Card): The card that is source of the effect.
        controller_index (int): Index of the player controlling the source card.
    """
    player = players[controller_index]
    if effect["type"] == "draw":
        for _ in range(effect["amount"]):
            draw_card(player)
    elif effect["type"] == "buff":
        source_card.power += effect["power"]
        source_card.toughness += effect["toughness"]
    elif effect["type"] == "damage":
        player["life"] -= effect["amount"]
    elif effect["type"] == "keyword":
        source_card.keywords.append(effect["keyword"])

def check_triggered_effects(event_type, player_index, opponent_index):
    """
    Checks all cards on the battlefield for triggered effects based on an event.

    Args:
        event_type (str): The event type to check triggers for.
        player_index (int): Index of the player whose battlefield to check.
        opponent_index (int): Index of the opponent.
    """
    player = players[player_index]
    for card in player["battlefield"]:
        if hasattr(card, "triggers"):
            for trigger in card.triggers:
                if event_type in trigger["trigger"]:
                    for effect in trigger["effects"]:
                        apply_effect(effect, card, player_index)

def get_tap_effect_from_text(text):
    """
    Extracts tap effect description from card's oracle text.

    Args:
        text (str): The oracle text of a card.

    Returns:
        str or None: The tap effect description or None if not found.
    """
    if not text:
        return None
    # Look for a line with "{T}:" indicating a tap ability
    for line in text.split('\n'):
        if line.strip().startswith("{T}:"):
            # Return the effect text after the tap cost
            return line.split(":", 1)[1].strip()
    return None

def handle_enter_the_battlefield(card, player):
    """
    Handles effects triggered when a card enters the battlefield.

    Args:
        card (Card): The card entering the battlefield.
        player (dict): The player who controls the card.
    """
    text = getattr(card, "oracle_text", "").lower()
    import re
    if "gain" in text and "life" in text:
        match = re.search(r"gain (\d+) life", text)
        if match:
            amount = int(match.group(1))
            addlife(player, amount)
            print(f"{card.name} ETB: Player gains {amount} life.")

    if "draw" in text and "card" in text:
        match = re.search(r"draw (\d+)? card", text)
        try:
            count = int(match.group(1) or 1)
        except:
            count = 1
        for _ in range(count):
            draw_card(players[player])
            print(f"{card.name} ETB: Draw {count} card(s).")

def trigger_card_effect(card, player):
    """
    Triggers the effect of a card.

    Args:
        card (Card): The card whose effect is triggered.
        player (dict): The player who controls the card.
    """
    opponent = players[1 - current_player]
    effect = parse_effect(card.oracle_text)
    apply_effect(effect, card, player)

def add_keyword_menu(card):
    """
    Opens a menu to add keywords to a card.

    Args:
        card (Card): The card to add keywords to.
    """
    keywords = ["flying", "first strike", "double strike", "trample", "lifelink", "deathtouch", "haste", "vigilance"]
    font = pygame.font.SysFont(None, 24)
    
    width, height = 180, 30
    x, y = 100, 100  # fixed menu position or customize
    
    menu_rects = []
    for i, kw in enumerate(keywords):
        rect = pygame.Rect(x, y + i * height, width, height)
        menu_rects.append((rect, kw))
    
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for rect, kw in menu_rects:
                    if rect.collidepoint(mx, my):
                        card.keywords.add(kw)
                        print(f"Added keyword '{kw}' to {card.name}")
                        selecting = False
                        break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                selecting = False
        
        pygame.draw.rect(screen, (50, 50, 70), (x, y, width, height * len(keywords)))
        for rect, kw in menu_rects:
            pygame.draw.rect(screen, (70, 70, 100), rect)
            text_surf = font.render(kw, True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + 5, rect.y + 5))
        
        pygame.display.flip()
        clock.tick(30)


def add_counters_menu(card):
    """
    Opens a menu to add +1/+1 counters to a creature.

    Args:
        card (Creature): The creature card to add counters to.
    """
    font = pygame.font.SysFont(None, 24)
    width, height = 180, 30
    x, y = 400, 100  # fixed menu position or customize
    
    # Counters to add - you can expand this list
    counters = [1, 2, 3, 4, 5]
    menu_rects = []
    for i, cnt in enumerate(counters):
        rect = pygame.Rect(x, y + i * height, width, height)
        menu_rects.append((rect, cnt))
    
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for rect, cnt in menu_rects:
                    if rect.collidepoint(mx, my):
                        # Add +1/+1 counters
                        if hasattr(card, "power") and hasattr(card, "toughness"):
                            card.power += cnt
                            card.toughness += cnt
                            print(f"Added {cnt} +1/+1 counter(s) to {card.name}")
                        selecting = False
                        break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                selecting = False
        
        pygame.draw.rect(screen, (50, 50, 70), (x, y, width, height * len(counters)))
        for rect, cnt in menu_rects:
            pygame.draw.rect(screen, (70, 70, 100), rect)
            text_surf = font.render(f"+{cnt}/+{cnt} counter(s)", True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + 5, rect.y + 5))
        
        pygame.display.flip()
        clock.tick(30)

def show_select_menu(card, pos):
    """
    Displays a menu at a position for card interactions like adding keywords or counters.

    Args:
        card (Card): The card to modify.
        pos (tuple): (x, y) position for menu display.
    """
    # pos = (x, y) for menu location (mouse click)
    menu_items = ["Add Keyword", "Add +1/+1 Counter"]
    font = pygame.font.SysFont(None, 24)
    
    # Create rects for menu items
    menu_rects = []
    width = 180
    height = 30
    x, y = pos
    for i, item in enumerate(menu_items):
        rect = pygame.Rect(x, y + i * height, width, height)
        menu_rects.append((rect, item))
    
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for rect, item in menu_rects:
                    if rect.collidepoint(mx, my):
                        selecting = False
                        if item == "Add Keyword":
                            add_keyword_menu(card)
                        elif item == "Add +1/+1 Counter":
                            add_counters_menu(card)
                        break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                selecting = False
        
        # Draw menu background
        pygame.draw.rect(screen, (50, 50, 70), (x, y, width, height * len(menu_items)))
        
        # Draw menu items
        for rect, item in menu_rects:
            pygame.draw.rect(screen, (70, 70, 100), rect)
            text_surf = font.render(item, True, (255, 255, 255))
            screen.blit(text_surf, (rect.x + 5, rect.y + 5))
        
        pygame.display.flip()
        clock.tick(30)


def activate_planeswalker_ability(player, planeswalker, ability_index):
    """
    Activates a specified ability of a planeswalker if possible.

    Args:
        player (dict): The player controlling the planeswalker.
        planeswalker (Planeswalker): The planeswalker object.
        ability_index (int): The index of the ability to activate.
    """
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

def activate_artifact(card, player):
    """
    Activates an artifact's effect based on its oracle text.

    Args:
        card (Card): The artifact card.
        player (dict): The player activating the artifact.
    """
    if not hasattr(card, "oracle_text") or not card.oracle_text:
        return
    text = card.oracle_text.lower()
    import re
    print(text)
    if "tap:" in text and "add {" in text and not card.is_tapped:
        match = re.search(r"add {([gubrw])}", text)
        if match:
            color = match.group(1).upper()
            tap_land(player, card, 1, color)


def untap():
    """
    Untaps all permanents and resets mana activation for current player.
    """
    resetmana(players[current_player])
    for card in players[current_player]["battlefield"]:
        card.is_tapped = False
        if isinstance(card, Planeswalker):
            card.has_activated_ability = False

def draw_phase():
    """
    Executes the draw step for the current player.
    """
    draw_card(players[current_player])

def main_phase():
    pass

# Define the sequence of game phases
phases = [untap, draw_phase, main_phase, combat_phase, combat_resolution_phase]
current_phase = 0  # Index to track current phase

# Load decks for each player and draw initial hands
for p in players:
    p["library"] = load_deck(p["deck"])  # Load deck data from file
    for _ in range(7):
        draw_card(p)  # Draw opening hand of 7 cards

# Initialize variables for card dragging mechanics
dragging_card = None
offset_x = offset_y = 0

# Main game loop
running = True
while running:
    # Clear the screen each frame
    screen.fill((33, 30, 40))
    
    # Process all queued events (mouse, keyboard, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game loop on window close

        # Left mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if selecting_attackers:
                # Select creatures to attack
                for card in players[current_player]["battlefield"]:
                    if card.rect.collidepoint(event.pos) and not card.is_tapped and isinstance(card, Creature):
                        card.is_tapped = True  # Tap creature for attack
                        attackers.append(card)
                # Transition to blocking phase
                selecting_attackers = False
                selecting_blockers = True

            elif selecting_blockers:
                # Select blockers for attacking creatures
                count = 0
                for card in players[1 - current_player]["battlefield"]:
                    if card.rect.collidepoint(event.pos) and not card.is_tapped and isinstance(card, Creature):
                        count += 1
                        blockers[count] = card
                        for atk in attackers:
                            if atk not in blockers:
                                blockers[atk] = card
                                card.is_tapped = True  # Tap blocker
                                break
                # End blocker selection
                selecting_blockers = False

            elif selected_planeswalker:
                # If a planeswalker ability menu is open
                for rect, ability_text in ability_buttons:
                    if rect.collidepoint(event.pos):
                        # Activate selected ability
                        apply_planeswalker_ability(selected_planeswalker, ability_text, players[current_player])
                        selected_planeswalker.has_activated_ability = True
                        selected_planeswalker = None  # Close menu
                        ability_buttons.clear()
                        break

            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # Shift-click to delete cards from zones
                for zone in ["battlefield", "hand"]:
                    for card in players[current_player][zone]:
                        if card.rect.collidepoint(event.pos):
                            # Remove card from zone
                            players[current_player][zone].remove(card)
                            print(f"Deleted {card.name} from {zone}")
                            break  # Exit after deleting one card
                continue  # Skip further processing for this event

            else:
                # Check if a planeswalker card was clicked to open abilities menu
                for card in players[current_player]["battlefield"]:
                    if isinstance(card, Planeswalker) and card.rect.collidepoint(event.pos):
                        if not card.has_activated_ability:
                            # Prepare ability buttons for display
                            selected_planeswalker = card
                            ability_buttons.clear()
                            for i, ability in enumerate(card.abilities):
                                btn_rect = pygame.Rect(card.rect.x, card.rect.y - (i + 1) * 30, 200, 25)
                                ability_buttons.append((btn_rect, ability))
                    # Check if a creature was clicked to show context menu
                    if card.rect.collidepoint(event.pos) and isinstance(card, Creature):
                        show_select_menu(card, event.pos)
                        break

                # Check if a hand card was clicked for dragging or casting
                for card in players[current_player]["hand"]:
                    # Parse effects and triggers for the card
                    card.effects = parse_effect(card.oracle_text)
                    card.triggers = [e for e in card.effects if e["type"] == "trigger"]
                    if card.rect.collidepoint(event.pos):
                        if phases[current_phase] == main_phase:
                            dragging_card = card  # Start dragging
                            offset_x = card.rect.x - event.pos[0]
                            offset_y = card.rect.y - event.pos[1]

                            # If the card is a land, place it directly
                            if "land" in card.card_type:
                                if not landplaced:
                                    landplaced = True
                                    # Apply effects (like adding mana) for land placement
                                    for effect in parse_effect(dragging_card.oracle_text):
                                        apply_effect(effect, dragging_card, current_player)
                            else:
                                # For spells/creatures, check mana cost
                                cost_list = parse_mana_cost(dragging_card.mana_cost)
                                if can_pay_cost(cost_list, players[current_player]["mana_pool"]):
                                    # Pay mana and cast card
                                    pay_cost(cost_list, players[current_player]["mana_pool"])
                                    for effect in parse_effect(dragging_card.oracle_text):
                                        apply_effect(effect, dragging_card, current_player)
                                else:
                                    print("Not enough mana to cast", dragging_card.name)
                            break

        # Right mouse button down: tap land or tap cards
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for card in players[current_player]["battlefield"]:
                if card.rect.collidepoint(event.pos) and not card.is_tapped:
                    name = card.name.lower()
                    # Auto-tap if it's a land
                    if "Land" in card.card_type:
                        tap_land(players[current_player], card, 1, 
                                 "G" if "forest" in name else
                                 "U" if "island" in name else
                                 "R" if "mountain" in name else
                                 "B" if "swamp" in name else
                                 "W" if "plains" in name else "C")
                    # Tap effect if text contains tap trigger
                    if "{T}" in card.oracle_text or "tap:" in card.oracle_text.lower():
                        card.is_tapped = True
                        for effect in parse_effect(card.oracle_text):
                            print(effect)
                            apply_effect(effect, card, current_player)
                    card.is_tapped = True

        # Middle mouse button down: untap tapped cards
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for card in players[current_player]["battlefield"]:
                if card.rect.collidepoint(event.pos) and card.is_tapped:
                    card.is_tapped = False

        # Mouse button release: place dragged card on battlefield or in hand
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging_card:
                # Determine if dropped in player's battlefield zone
                drop_zone = (
                    (current_player == 0 and HEIGHT // 2 < dragging_card.rect.y < HEIGHT) or
                    (current_player == 1 and 0 < dragging_card.rect.y < HEIGHT // 2)
                )

                if drop_zone:
                    # If a land, place on battlefield if not already placed
                    if "land" in dragging_card.card_type.lower():
                        if not landplaced:
                            landplaced = True
                            players[current_player]["battlefield"].append(dragging_card)
                            if dragging_card in players[current_player]["hand"]:
                                players[current_player]["hand"].remove(dragging_card)
                            for effect in parse_effect(dragging_card.oracle_text):
                                apply_effect(effect, dragging_card, current_player)
                    else:
                        # For spells/creatures, cast by paying mana
                        cost_list = parse_mana_cost(dragging_card.mana_cost)
                        if can_pay_cost(cost_list, players[current_player]["mana_pool"]):
                            pay_cost(cost_list, players[current_player]["mana_pool"])
                            if dragging_card in players[current_player]["hand"]:
                                players[current_player]["hand"].remove(dragging_card)
                            players[current_player]["battlefield"].append(dragging_card)
                            for effect in parse_effect(dragging_card.oracle_text):
                                apply_effect(effect, dragging_card, current_player)
                        else:
                            print("Not enough mana to cast", dragging_card.name)
                dragging_card = None  # Reset drag state

        # Mouse movement while dragging a card
        elif event.type == pygame.MOUSEMOTION:
            if dragging_card:
                dragging_card.rect.x = event.pos[0] + offset_x
                dragging_card.rect.y = event.pos[1] + offset_y

        # Keyboard input handling
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Move to next phase
                current_phase = (current_phase + 1) % len(phases)
                phases[current_phase]()  # Execute phase function
                # Handle turn switch after resolution phase
                if phases[current_phase] == combat_resolution_phase:
                    if current_player < 1:
                        current_player += 1
                    else:
                        current_player = 0
                # Reset land placement for new turn
                if phases[current_phase] == untap:
                    landplaced = False

            elif event.key == pygame.K_d:
                # Draw a card
                draw_card(players[current_player])

            elif event.key == pygame.K_SPACE:
                # End turn: switch player and reset states
                current_player = current_player
                landplaced = False
                resetmana(players[current_player])
                for card in players[current_player]["battlefield"]:
                    card.is_tapped = False
                print(f"Player {current_player + 1}'s turn")

            # Play first card in hand (simplified)
            elif event.key in [pygame.K_e, pygame.K_RETURN]:
                player = players[current_player]
                hand = player["hand"]
                if hand:
                    selected = hand[0]
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

            # Tap first untapped land
            elif event.key in [pygame.K_t]:
                player = players[current_player]
                for card in player["battlefield"]:
                    if "Land" in card.card_type and not card.is_tapped:
                        name = card.name.lower()
                        tap_land(player, card, 1, 
                                 "G" if "forest" in name else
                                 "U" if "island" in name else
                                 "R" if "mountain" in name else
                                 "B" if "swamp" in name else
                                 "W" if "plains" in name else "C")
                        
            # Mana and life modifications via number keys
            elif event.key == pygame.K_0:
                add_to_pool(players[current_player], 1, "G")
            elif event.key == pygame.K_9:
                add_to_pool(players[current_player], 1, "R")
            elif event.key == pygame.K_8:
                add_to_pool(players[current_player], 1, "U")
            elif event.key == pygame.K_7:
                add_to_pool(players[current_player], 1, "B")
            elif event.key == pygame.K_6:
                add_to_pool(players[current_player], 1, "W")
            elif event.key == pygame.K_5:
                add_to_pool(players[current_player], 1, "C")
            elif event.key == pygame.K_l:
                addlife(players[current_player], 1)
            elif event.key == pygame.K_j:
                addlife(players[current_player], -1)

            # Discard a card
            elif event.key == pygame.K_f:
                discard_card(players[current_player])

            # Buff a creature (placeholder, assumes 'card' is defined)
            elif event.key == pygame.K_b:
                buff_creature(card, 1, 1)

            elif event.key == pygame.K_q:
                # Placeholder for other actions
                pass

    # Check for player death
    if players[current_player]["Health"] <= 0:
        # Display death message
        screen.blit(font.render(f"Player {current_player+1} has died", True, (255,255,255)), (500, 500))

    # Display current game stats
    screen.blit(font.render(f"Player 2: {players[1]['Health']}", True, (255,255,255)), (20, 10))
    screen.blit(font.render(f"Player 1: {players[0]['Health']}", True, (255,255,255)), (20, HEIGHT - 180))
    screen.blit(font.render(f"Current Turn: Player {current_player + 1}", True, (255,255,255)), (WIDTH // 2 - 100, 10))
    screen.blit(font.render(f"Phase: {['Untap', 'Draw', 'Main', 'Combat', 'Resolution'][current_phase]}", True, (255,255,255)), (WIDTH // 2 - 100, 40))

    # Draw hands, battlefield, and mana pools
    draw_hand(players[0]["hand"], HEIGHT - 150, current_player == 0)
    draw_hand(players[1]["hand"], 50, current_player == 1)
    draw_battlefield(players[0]["battlefield"], HEIGHT // 2 + 80)
    draw_battlefield(players[1]["battlefield"], HEIGHT // 2 - 220)
    draw_mana_pool(players[0]["mana_pool"], WIDTH - 150, HEIGHT - 200)
    draw_mana_pool(players[1]["mana_pool"], WIDTH - 150, 80)

    # Draw combat animations (damage lines)
    handle_combat_animations()

    # Show ability buttons if a planeswalker is selected
    if selected_planeswalker:
        for rect, text in ability_buttons:
            pygame.draw.rect(screen, (70, 70, 100), rect)
            screen.blit(font.render(text, True, (255, 255, 255)), (rect.x + 5, rect.y + 5))

    # Update display and tick clock for frame rate
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
