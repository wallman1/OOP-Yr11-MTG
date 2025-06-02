import pygame
class Card:
    def __init__(self, name, power, toughness, card_type, image_path=None, mana_cost=""):
        self.name = name
        self.power = power
        self.toughness = toughness
        self.mana_cost = mana_cost
        self.card_type = card_type
        self.image_path = image_path
        self.rect = pygame.Rect(0, 0, 100, 140)
        self.is_tapped = False

class Creature(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deathtouch = False
        self.lifelink = False

class Land(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mana_types = []  # Could be ["G"], ["U", "R"], etc.

class Sorcery(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.effect = None  # You can store a function or string here

class Instant(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Enchantment(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Artifact(Card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

