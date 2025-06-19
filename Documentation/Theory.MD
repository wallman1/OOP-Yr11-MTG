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

## Start of Sprint Potential Improvements
In starting Sprint 4, several significant additions have been identified to be made to the functionality and playability of the Magic: The Gathering collectible card game simulator. Among the largest areas of concentration is the full integration of triggered effects—more specifically those that occur when a card comes into play (ETB effects, as they are more commonly referred to). These include effects such as drawing cards, gaining life, or modifying creature stats the moment a card is played. Other enhancements include more apparent combat graphics, such as highlighting tapped cards and graphically linking attackers to blockers. The graveyard zone will also be shown, so players can monitor destroyed or discarded cards throughout a game. 
### Parsing System Enhancements
Enhancements to the parsing system will allow the system to better understand keyword abilities like lifelink, deathtouch, and haste. Furthermore, a core stack system will be implemented for managing the order and resolution of activated and triggered effects.

### Integration with Existing Codebase
The enhancements will be integrated into the existing codebase via modular extensions to current systems. The parse_effect() function, already utilized for pulling out card effects, will be expanded to also identify ETB triggers and other conditional effects. They will be stored as structured data in each card's triggers attribute and processed automatically whenever a card is entering the battlefield. For combat and visual updates, there will be new drawing logic added to the draw_card_image() and handle_combat_animations() functions, but without altering core rendering logic. The visible graveyard will be completed the same way as the hand and battlefield areas to ensure user interface consistency. In order to handle effect resolution, a global stack list will be maintained and resolved in the resolution phase. This step-by-step methodology ensures that enhancements can be completed incrementally while preserving stability and backwards compatibility with the existing feature set.

## Sprint 4 Review
### Evaluation of Functional and Non-Functional Requirements

As of the end of Sprint 4, the project has met most of the functional requirements set during the planning stage. Most notable features such as turn-based mechanics, resolution of combat, generation of mana, and interaction of cards are all functioning as intended. Adding effect parsing and triggerd abilities (e.g., "enter the battlefield" effects and lifelink) greatly advanced the program's ability to simulate a game of Magic: The Gathering. The non-functional requirements, such as responsiveness, fullscreen support, and mouse-based interaction support, have also been fulfilled. The simulator runs stably at 30 FPS, does not consume any visible memory leaks, and provides a smooth gaming experience.

### Performance Against Key Use-Cases

Key use-cases—such as playing a creature, playing lands to acquire mana, attacking with creatures, and resolving Planeswalker abilities—are all correctly implemented. Cards now correctly trigger effects on entering the battlefield, such as lifegain and card draw, which were clearly defined in the original use-case tests. The game loop correctly interacts with input/output, logging the clicks for card choosing, drag-and-drop, and combat targeting as expected. The concept of a mana pool precludes wrong plays by allowing appropriate use of resources. During testing, all the use-case scenarios executed without crashes or unhandled exceptions, and user feedback indicated that basic gameplay flows were intuitive.

### Program Behaviour and Input/Output Handling

The program performs as desired in nearly all of the tested cases. Cards are dragnable, castable, and activatable with minimal bugs. Handling of input is responsive and accurate—mouse movement adequately maps to card locations, and the game behaves predictably in reaction to phase transitions and user input. The one issue is sporadic "ghost image" visibility when cards are being dragged, which could be related to improper handling of card rectangles during click-and-drag events. However, they don't make too much of a difference in gameplay.

### Code Quality: Readability, Structure, and Maintainability

Code is well-structured, modular and separates logic (e.g., parsing of effects, combat resolution) from rendering (e.g., draw_card_image, draw_hand). Naming conventions are good for the most part, and functions are well-scoped and named. Reusable and extensible regions are primary ones like parse_effect, apply_effect, and combat logic. Certain codebase recommendations would be enhanced by further readability-improving comments, especially where more complex functions like trigger resolution and event-based combat implementation are the case. Refactoring duplicated logic (for instance, card casting and event application) into smaller, more specialized helper functions can improve maintainability.

### The Next Development Stage Improvements

In case of additional complications, some of the key improvements are recommended. Feature-wise, the resolution mechanism for the stack can be expanded to allow for player response to spells and abilities and thus more realistic gameplay. Multiplayer or network functionality could also be included. From the code quality perspective, redundant logic needs to be refactored, and a more object-oriented design can be included, encapsulating player and game-stage logic within classes. Unit tests can be written to ensure important functions behave as expected under different conditions. Lastly, optimizing the card loading system to cache images and card information better would reduce overhead and improve scalability.

## Final Evaluation
### System Upgrades and Effect on Player Experience
There are several different ways that I could upgrade this Magic: The Gathering simulator in the future. One of the most significant would be adding a "stack" system. When a player in real Magic plays a spell or uses an ability, it is added into a stack where other players can reply. The game currently doesn't support that. Having a stack system would allow players to play more dynamically and make decisions on the basis of what their opponent is playing off of, for instance, counterspelling. This would more accurately mimic how it actually is in real life.

I can also make the interface richer with additional animations and sound. For example, flashing a lightning bolt icon when dealing damage, or an audio tap when a card is tapped. Effects like "draw a card" or "gain 1 life" just happen without any sound or visual effects, and this takes away from the game's entertainment factor. Additional visual feedback and sound effects would allow for greater accessibility and more enjoyment for players.

### Impact Analysis:
Positive impacts: These would make the game more enjoyable and more playable. The players would feel more in control and involved in what's happening. It would allow new players to pick up the rules more easily by showing cause and effect directly.

Negative effects: These additions would increase the game's complexity. Novice players might find the new features confusing at first. It would also slow down the game if not optimized, especially with extra animations or memory usage.

### Assessment of Requirements and Specifications
The system meets most of the functional and non-functional requirements established in the planning stage. According to the planning document, the primary goals were:

 - Give players the capacity to draw cards and build a battlefield

 - Give fighting with tapping, harm, and blockers

 - Give turn phases and mana control

 - Give abilities and effects through Oracle text (e.g., "draw a card", "+1/+1", "enter the battlefield")

These goals have been achieved. For example, cards can be drawn from the hand, mana is tracked, and effects burn properly when a card enters the battlefield. Planeswalker powers can be selected using a button configuration too. The game responds well to input and plays well in fullscreen mode, achieving the non-functional criteria of usability and performance.

Use-case testing reveals that all gameplay scenarios, such as summoning a creature, attacking, or playing a land, all work properly. A small bug is that occasionally a "ghost" image occurs when dragging cards, but it doesn't interrupt gameplay. In general, the game acts as intended and processes inputs and gameplay states properly. 

### Evaluation of Project Management
Looking back at my Gantt Chart, I had completed most of my milestones on or prior to the dates that I had established. Sprint 1 was establishing the interface and basic card handling, which I completed quickly. Sprint 2 was adding in phases, tap, and combat, which I completed ahead of schedule. Sprint 3 was longer because I was breaking down and coding the effects from the Oracle text, which was complex.

![alt text](/Documentation/Screenshot%202025-06-19%20194326.png)

Sprint 4 was spent refining and expanding on those effects and allowing for interactions like lifelink, triggered effects, and planeswalker assistance. These were completed mostly on time, although I was unable to include stack interaction due to time limitations.

Reflecting on my commit history and version history, I always delivered, enhancing aspects such as combat, triggered abilities, and responsiveness in the UI throughout sprints. My planning was also flexible, enabling me to make adjustments whenever new issues arose.

### Peer Evaluation and Feedback
Two of my peers tested my project and provided the following feedback in a PMI (Plus, Minus, Implication) format:



This feedback led me to realize that while the game logic is good, user interface and experience can be improved. In future development, better user feedback and greater visual or auditory guidance are required.

### Justification of Object-Oriented Programming (OOP) Features
This project was executed using the assistance of OOP (Object-Oriented Programming) to make the code easier to maintain, modify, and expand. I used classes to keep like data and behaviors together to make sure that I kept the game structure simple and easy to read.

#### Card Class
The Card class is the superclass of all types of cards. It has important properties like the card's name, card type, mana cost, oracle text, image, and screen position. It also has a rect that is used for collision detection through the mouse and is accessed throughout the game for events. All the other classes of cards inherit from this class, so all these properties are available to them. This is an example of how inheritance is applied, which is one of the basic OOP practices.

#### Creature(Card) Class
Creature is a subclass of Card and has attributes like power, toughness, is_tapped, and attacking. Creature also has combat interaction logic, for example, whether it can attack or block. Moving the creature into its own class meant I did not jam the base Card class with creature-related logic. This is encapsulation—organizing code according to function.

#### Planeswalker(Card) Class
Planeswalkers also have their own behaviors, i.e., loyalty points and special abilities that are used once a turn. This class contains loyalty and a flag to track if the ability was utilized. It also contains a list of ability texts, which are clickable buttons on the GUI. Having all of that be its own class allowed me to isolate the logic from regular cards and make it easier so that it's simpler to test. This also makes it possible for me to reuse this class with different planeswalker cards without reusing code.

#### Artifact(Card) Class
Artifacts are special cards with passive or activated effects. They also inherit from Card, so they also have the same display and interaction logic. Their own behavior, like tapping to produce mana or enhancing creatures, can be built on top. This enables me to work with new types of cards without altering the organization of the balance of the code. This is one instance of polymorphism—where a subclass such as Artifact can be substituted for the Card class but function differently.

#### Effect Parsing System
Effects like "draw a card", "gain 1 life", "tap: add {G}", and "when this enters the battlefield" are all handled by parsing the oracle text into dictionaries, and then applying them using a generic apply_effect() function. It's not a class itself, but it works with the classes to provide the system with dynamic and extensible behavior. It causes cards to behave differently based on their text without requiring special-case code for every one.

#### Conclusion on OOP
Using OOP made the project much easier to work with. Every card type is well-structured and has a clear purpose. I was able to implement new features like planeswalkers and effects effortlessly without needed to rewrite code. If I needed to implement other card types like instants or sorceries, I could create new classes in the same style. This tended to keep the code readable, testable, and reusable—exactly what good OOP design is meant to achieve.
