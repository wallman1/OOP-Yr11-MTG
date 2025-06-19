## Requirements
### Functional Requirements
#### Card Interaction
 - Players can draw, play, and tap cards.
 - Creatures can attack and block.
 - Oracle text cards have effects that automatically occur.
 - Lands tap to generate mana of appropriate colors.

#### Turn Structure
 - The game progresses in phases: Untap, Draw, Main, Combat, Resolution.
 - The current player can play lands and cast spells in the Main Phase.
 - Players can select attackers and blockers in the Combat.

#### Mana System
 - Players have a mana pool which gets replenished when lands are tapped.
 - Spells require valid mana costs to play.
 - Mana is withdrawn between phases by game rules.
#### Card Types & Effects
 - Supported: Creatures, Lands, Artifacts, Planeswalkers.
 - Oracle text is read and parsed to compute and apply card effects (e.g., "Draw a card", "+1/+1", "tap: Add {G}").
#### User Interaction
 - Cards are draggable.
 - Click and right-click handling supports tapping/untapping or playing abilities.
 - Planeswalker abilities show a menu on click.
#### Game State Display
 - Players' health, mana pool currently, turn phase, and battlefield are shown.
 - Messages (e.g., "Player 1 has died") on-screen.

### Non-Functional Requirements
#### Performance
 - Should be playable at 30 FPS minimum on regular hardware.
#### Portability
 - Runs on Windows, macOS, and Linux with Python and Pygame installed.
#### Usability
 - Easy-to-understand interface with mouse controls and keybinds.
 - Font and layout readable at fullscreen resolution.
#### Extensibility
 - Modular functionality and class-based design allow introducing new card types, mechanics, and functionality.
#### API Integration
 - Must use Scryfall API to load images and data of cards.

## Specifications
### Entities
Player: Health, hand, deck, battlefield, graveyard, mana pool.

Card: Name, type, oracle text, mana cost, image, is_tapped, power/toughness.

Creature, Planeswalker, Artifact, Land: Card subclasses.

Game: Tracks turn, phase, players, stack, selected card, selected planeswalker.

### Inputs
Mouse clicks (left/right/middle).

Mouse drag for card movement.

Keyboard shortcuts:

SPACE: Next phase

D: Draw

E/ENTER: Play first card

T: Tap first untapped land

0-5: Add specific mana to pool

L/J: Change life

F: Discard card

B: Buff creature

### Outputs
Visual display of cards, hand, battlefield, and mana pool.

Text indicators for:

Health values

Mana pool status

Current turn and phase

Notifications (e.g., "Not enough mana")

### Game Rules Handled
Mana cost check and payment.

Turn and phase progression.

Combat system (attackers/blockers).

Oracle text processing (tap effects, buffs, draw).

Win condition (player at 0 health).

### Optional Features (Planned Enhancements)
Game save/load functionality.

Online multiplayer.

AI opponent.

Improved stack resolving and triggered effects.

Card search window with filters.

## Use Case Diagram
![alt text](/Documentation/Screenshot%202025-06-18%20171914.png)

## Data Flow Diagram
![alt text](/Documentation/Screenshot%202025-06-18%20172735.png)

## Gantt Chart
![alt text](/Documentation/Screenshot%202025-06-18%20195407.png)

## Sprint 1 Review
Throughout Sprint One, the project demonstrated high adherence to the initial set of functional and non-functional requirements outlined in the planning process. Key functionalities like showing Magic: The Gathering cards on the battlefield, moving cards from hand to battlefield, tapping creatures to identify attackers, and casting Planeswalker abilities were successfully achieved. The oracle text parsing system also executed well basic tasks like "draw a card" and "deal damage." As far as non-functional goals are concerned, the program also exhibited good responsiveness and visual simplicity. There was a slight decrease in performance when multiple visual elements like menus were displayed at the same time.

The system worked well with respect to main use-cases identified in the initial planning phase. For instance, user actions such as dragging cards, tapping to attack, and blocking functioned as expected. Turn-based switching from main phase to combat phase was natural, and triggered effects such as drawing cards were included, although some problems related to controller indexing and effect targeting were identified. Planeswalker ability activation through a menu item in-game functioned exactly as expected, with proper integration of both UI and underlying code. Most of the program's behavior was as predicted, but additional input validation and error checking will be needed to deal with edge cases and unmapped inputs.

Input and output management was generally successful. Mouse input—i.e., clicks to select and drag events—elicited responses as intended, and output was correctly reported through on-screen state alteration and console-printed return. While overall interactions were intuitive, there were some instances where there was conflicting input or feedback that was visually inaccessible. This will be addressed in subsequent development phases.

The current code is a decent starting point, with fundamental logic encapsulated in well-named functions like apply_effect, parse_effect, and handle_enter_the_battlefield. Overall, the codebase can be enhanced in terms of organization and readability. The naming convention is inconsistent in using camelCase and snake_case, making it more difficult to read. Comments and documentation are mostly missing, especially in more complex areas like combat resolution and trigger handling. Moreover, there is minimal redundant or highly nested code that can be refactored for improved maintainability and scalability when the game complexity grows.

As Sprint Two looks ahead, feature additions and structural optimization are planned. On the gameplay side, adding a stack system in order to process triggered abilities efficiently in a stacked fashion will improve rule precision. Adding support for the effect parser to deal with more advanced oracle text and keyword powers is also a priority. Other new features can be simple AI or multiplayer ability, as well as improved GUI feedback for incorrect actions like playing a second land or attempting to play a spell that requires too much mana. In terms of code quality, the plan is to refactor the project into neater modules, enforce standard naming conventions, and include greater documentation and inline comments to make maintenance and collaboration easier in the future.

In total, Sprint One laid a strong foundation for an operable MTG simulator. The program shows promising improvement towards meeting all requirements stated, and through diligent additions, it is very apt for more advanced features and more polish in the next sprint.

## Structure Chart
![alt text](/Documentation/Screenshot%202025-06-18%20200331.png)

## Pseudocode
### Main Loop
procedure MAIN_GAME_LOOP

    initialize_game()

    while running is True

        handle_events()

        process_game_phase()
        
        render_game()

        check_win_condition()

    end while

end procedure

### Subroutine 1
procedure HANDLE_EVENTS

    for each event in pygame_event_queue

        if event is QUIT

            set running to False

        else if event is mouse_click

            if over_card and in_hand

                if card is land

                    play_land(card)

                else

                    if can_pay_cost(card)

                        cast_spell(card)

        else if event is key_press

            if key is SPACE

                advance_to_next_phase()

            else if key is D

                draw_card(current_player)

end procedure

### Subroutine 2
function load_deck(filename):

    initialize empty list called deck

    open file with name 'filename' in read mode

        read the contents of the file as JSON

        for each card_data in the JSON list:

            call get_card_data(card_data["name"])  // retrieve card details from API or cache

            if card_data["type_line"] contains "Creature":

                create creature object with retrieved data

            else if card_data["type_line"] contains "Artifact":

                create artifact object with retrieved data

            else if card_data["type_line"] contains "Planeswalker":

                create planeswalker object with retrieved data

            else:

                create generic card object with retrieved data

            add the created card object to deck

    return deck


## Flowcharts
### Main Loop
![alt text](/Documentation/Screenshot%202025-06-18%20201318.png)

### Subroutine 1
![alt text](/Documentation/Screenshot%202025-06-18%20201629.png)

### Subrountine 2
![alt text](/Documentation/Screenshot%202025-06-18%20202013.png)

## Sprint 2 Review
During Sprint 2, the project achieved considerable advancement toward meeting both functional and non-functional requirements set out during planning. Key functional goals such as Planeswalker ability activation, triggered effects (e.g., drawing a card when a creature enters the battlefield), and a graphical ability selection menu were successfully implemented. These features directly correspond to expectations set in the requirements document, particularly those discussing card interaction depth and more developed game mechanics. Non-functional requirements like responsiveness and minimal user feedback (e.g., visual cues and ability highlighting) were also partially addressed, which improved usability.

The program behaved as anticipated across key use cases such as casting spells, triggering abilities, resolving effects, and transitioning between phases. It appropriately detected triggers such as "when this creature enters the battlefield" or "when you draw a card" and responded with the correct output (e.g., drawing a card or applying buffs), which aligned with the expected system behavior. Input through mouse interactions also worked as anticipated, especially in card dragging, targeting, and ability activation.

Code quality improved from Sprint 1, with greater modular design and more consistent function usage. Naming conventions were more readable, and some duplicated logic (e.g., trigger checking) was extracted into reusable functions. Parts of the codebase still have highly nested if-statements and a lack of thorough documentation. Further cleanup is required to make the system more maintainable, such as refactoring duplicated logic and including more comments for describing function responsibilities.

For Sprint 3, the areas for improvement should be directed at polishing the triggered ability system, implementing the stack for spell and ability resolution, and continuing to develop the UI for improved game state representation. Code organization is also worth consideration, such as maintaining concerns separately (like separating UI handling and game logic) and improving test coverage. These will enable smoother development in future sprints and push the project further towards full feature readiness.

## UML Diagram
![alt text](/Documentation/Untitled.png)

## Sprint 3 Review
During Sprint 3, the project continued to develop effectively, addressing many of the functional and non-functional requirements outlined during the planning phase. Core gameplay features, including counter addition, triggered card draw when taking damage, and expanded effect parsing, were implemented and integrated smoothly with the existing game loop. This directly aligns with functional expectations defined in the requirements, such as supporting more advanced Magic: The Gathering mechanics and improving the player interaction system. Non-functional goals such as responsiveness and user clarity were also addressed through visual feedback improvements and more intuitive menus.

The program successfully handled most key use-cases, such as adding counters to creatures, managing triggered abilities during combat, and allowing users to interact with a menu for selecting abilities or adding effects. Input handling through mouse events worked as intended, and output responses (e.g. card animations, tapped states, card drawing) matched the expected outcomes. This demonstrates that the system is responding well under multiple game scenarios and provides a solid base for further complexity.

Code quality continued to improve in Sprint 3. Naming conventions remained consistent, and functions were written with better separation of concerns. Complex effects were broken into subroutines, which improves readability and maintainability. However, the code still contains some tight coupling between the UI and game logic, and deeper documentation is needed to support long-term scalability. While comments have improved, some sections (especially newer functions) still lack detailed explanations.

Looking ahead to the next stage, improvements should focus on implementing a basic stack system for managing triggered and activated abilities, improving save/load functionality, and enhancing card search and filtering features. Structurally, further refactoring should aim to decouple UI rendering from game mechanics, introduce a clearer event system, and better organize the codebase into modular files. These changes will not only improve performance and maintainability but also enable more complex interactions in future updates.