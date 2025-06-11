import pygame
class Card:
    def __init__(self, name, power, toughness, card_type, image_path, mana_cost, oracle_text=""):
        self.name = name
        self.power = power
        self.toughness = toughness
        self.card_type = card_type
        self.image_path = image_path
        self.mana_cost = mana_cost
        self.oracle_text = oracle_text
        self.rect = pygame.Rect(0, 0, 100, 140)
        self.is_tapped = False
        self.keywords = self.extract_keywords()
        self.keywords = []

    def extract_keywords(self):
        keywords = []
        if "flying" in self.oracle_text.lower():
            keywords.append("flying")
        if "trample" in self.oracle_text.lower():
            keywords.append("trample")
        if "first strike" in self.oracle_text.lower():
            keywords.append("first strike")
        return keywords
        

class Creature(Card):
    pass

class Artifact(Card):
    def __init__(self, name, mana_cost, image_path):
        super().__init__(name, "Artifact", mana_cost, image_path)
        # Add artifact-specific attributes here

class Planeswalker(Card):
    def __init__(self,name,power, toughness, mana_cost, image_path, loyalty, abilities):
        super().__init__(power, toughness, name, "Planeswalker", mana_cost, image_path)
        self.loyalty = loyalty
        self.abilities = abilities
        self.has_activated_ability = False

