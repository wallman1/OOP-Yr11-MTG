import json

class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, name):
        self.cards = [card for card in self.cards if card.name != name]

    def save(self, path="decks/my_deck.json"):
        with open(path, "w") as f:
            json.dump([card.__dict__ for card in self.cards], f)

    def load(self, path="decks/my_deck.json"):
        with open(path, "r") as f:
            data = json.load(f)
            from card import Card
            self.cards = [Card(**d) for d in data]