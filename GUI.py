import pygame
import sys
from Api import search_cards, get_image_from_url, save_to_deck, load_deck, search_cards_exact

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("MTG Deck Builder")
font = pygame.font.SysFont(None, 32)
large_font = pygame.font.SysFont(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (70, 70, 70)
BLUE = pygame.Color('dodgerblue2')
DARK = (25, 25, 25)

# States
HOME, SEARCH, DECKS, DECK_VIEW = "HOME", "SEARCH", "DECKS", "DECK_VIEW"
state = HOME

# Input box setup
input_box = pygame.Rect(100, 100, 600, 40)
deck_input_box = pygame.Rect(100, 160, 600, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = BLUE
color = color_inactive
active = False
deck_active = False
text = ''
deck_name = ''
search_results = []
selected_card = None
card_image = None
deck_cards = []
current_deck = ''

# Buttons
search_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
decks_button = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)
back_button = pygame.Rect(20, 20, 100, 40)
save_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
load_deck_buttons = []

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(DARK)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == HOME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if search_button.collidepoint(event.pos):
                    state = SEARCH
                elif decks_button.collidepoint(event.pos):
                    deck_cards = list(load_deck())
                    load_deck_buttons = [pygame.Rect(100, 140 + i * 50, 600, 40) for i in range(len(deck_cards))]
                    state = DECKS

        elif state == SEARCH:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    deck_active = False
                elif deck_input_box.collidepoint(event.pos):
                    deck_active = True
                    active = False
                else:
                    active = False
                    deck_active = False

                color = color_active if active else color_inactive

                if back_button.collidepoint(event.pos):
                    state = HOME
                    search_results = []
                    selected_card = None
                    card_image = None

                if 220 < event.pos[1] < 520:
                    index = (event.pos[1] - 220) // 60
                    if index < len(search_results):
                        selected_card = search_results[index]
                        if 'image_uris' in selected_card:
                            img_url = selected_card['image_uris']['png']
                            if get_image_from_url(img_url):
                                card_image = pygame.image.load("image.png")

                if save_button.collidepoint(event.pos):
                    save_to_deck(selected_card['name'])

            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        search_results = search_cards(text)
                        selected_card = None
                        card_image = None
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                elif deck_active:
                    if event.key == pygame.K_BACKSPACE:
                        deck_name = deck_name[:-1]
                    else:
                        deck_name += event.unicode

        elif state == DECKS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    state = HOME
                for i, btn in enumerate(load_deck_buttons):
                    if btn.collidepoint(event.pos):
                        current_deck = deck_cards[i]
                        deck_cards = load_deck()
                        state = DECK_VIEW

        elif state == DECK_VIEW:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    state = DECKS

    # --- Drawing ---
    if state == HOME:
        title = large_font.render("Magic: The Gathering Deck Builder", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        pygame.draw.rect(screen, BLUE, search_button)
        label = font.render("Start Searching", True, WHITE)
        screen.blit(label, (search_button.x + 30, search_button.y + 15))

        pygame.draw.rect(screen, BLUE, decks_button)
        decks_label = font.render("View Decks", True, WHITE)
        screen.blit(decks_label, (decks_button.x + 50, decks_button.y + 15))

    elif state == SEARCH:
        pygame.draw.rect(screen, GREY, back_button)
        back_text = font.render("Back", True, WHITE)
        screen.blit(back_text, (back_button.x + 10, back_button.y + 10))

        txt_surface = font.render(text, True, color)
        input_box.w = max(400, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        deck_surface = font.render(deck_name, True, color_active if deck_active else color_inactive)
        screen.blit(deck_surface, (deck_input_box.x + 5, deck_input_box.y + 5))
        pygame.draw.rect(screen, color_active if deck_active else color_inactive, deck_input_box, 2)

        for i, card in enumerate(search_results[:5]):
            y = 220 + i * 60
            pygame.draw.rect(screen, GREY, (100, y, 600, 50))
            name_surf = font.render(card['name'], True, WHITE)
            screen.blit(name_surf, (110, y + 10))

        if selected_card and card_image:
            scaled_img = pygame.transform.scale(card_image, (488, 680))
            screen.blit(scaled_img, (WIDTH // 2 - 244, HEIGHT - 740))

            pygame.draw.rect(screen, BLUE, save_button)
            save_text = font.render("Save to Deck", True, WHITE)
            screen.blit(save_text, (save_button.x + 30, save_button.y + 15))

    elif state == DECKS:
        screen.blit(large_font.render("Your Decks", True, WHITE), (WIDTH // 2 - 100, 60))
        pygame.draw.rect(screen, GREY, back_button)
        back_text = font.render("Back", True, WHITE)
        screen.blit(back_text, (back_button.x + 10, back_button.y + 10))

        for i, name in enumerate(deck_cards):
            pygame.draw.rect(screen, GREY, load_deck_buttons[i])
            name_surf = font.render(name, True, WHITE)
            screen.blit(name_surf, (load_deck_buttons[i].x + 10, load_deck_buttons[i].y + 10))

    elif state == DECK_VIEW:
        screen.blit(large_font.render(f"Deck: {current_deck}", True, WHITE), (WIDTH // 2 - 100, 60))
        pygame.draw.rect(screen, GREY, back_button)
        back_text = font.render("Back", True, WHITE)
        screen.blit(back_text, (back_button.x + 10, back_button.y + 10))

        for i, name in enumerate(deck_cards):
            y = 120 + i * 40
            name_surf = font.render(name, True, WHITE)
            screen.blit(name_surf, (100, y))

            if 100 <= mouse_pos[0] <= 700 and y <= mouse_pos[1] <= y + 40:
                try:
                    temp = search_cards_exact(name)
                    if temp and 'image_uris' in temp[0]:
                        if get_image_from_url(temp[0]['image_uris']['png']):
                            hover_img = pygame.image.load("image.png")
                            scaled_hover = pygame.transform.scale(hover_img, (244, 340))
                            screen.blit(scaled_hover, (WIDTH - 260, 120))
                except Exception as e:
                    print(f"Hover image error: {e}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

