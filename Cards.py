# card.py
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
        self.dragging = False
        self.is_tapped = False
