import pygame
class Card:
    def __init__(self, name, card_type, image_path, mana_cost, oracle_text=""):
        self.name = name
        self.card_type = card_type
        self.image_path = image_path
        self.mana_cost = mana_cost
        self.oracle_text = oracle_text
        self.rect = pygame.Rect(0, 0, 100, 140)
        self.is_tapped = False
        

class Creature(Card):
    def __init__(self, name, image_path, mana_cost, power, toughness):
        super().__init__(name, "Creature", image_path, mana_cost)
        self.power = power
        self.toughness = toughness
        self.keywords = set()
class Artifact(Card):
    def __init__(self, name, image_path, mana_cost, oracle_text=""):
        super().__init__(name, "Artifact", image_path, mana_cost, oracle_text="")
        self.oracle_text = oracle_text
        # Add artifact-specific attributes here

class Planeswalker(Card):
    def __init__(self, name, mana_cost, image_path, loyalty, abilities):
        super().__init__(name, "Planeswalker", image_path, mana_cost)
        self.loyalty = loyalty
        self.abilities = abilities
        self.has_activated_ability = False
