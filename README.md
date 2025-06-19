# Magic: The Gathering Simulator (Python + Pygame)

A fully functional Magic: The Gathering tabletop simulator built in Python using the Pygame library. It supports interactive gameplay between two players, including combat, mana management, turn phases, card casting, and the use of abilities parsed from Oracle text.

---

## Features

- Drag-and-drop card placement and battlefield management  
- Full turn-based system with phases (Untap, Draw, Main, Combat, Resolution)  
- Mana pool tracking with cost enforcement  
- Support for Creatures, Lands, Artifacts, and Planeswalkers  
- Card abilities parsed and applied from Oracle text  
- Triggered effects (e.g. "When this enters the battlefield...")  
- Tap-to-activate mechanics for mana and abilities  
- Damage calculation and combat resolution  
- UI rendering of mana pools, health, phases, and active turn  
- Shift+click card deletion for debugging or test environments  
- Fullscreen interface and scalable layout  
- Support for Scryfall API integration (in external file)

---

## How to Play

1. **Start the Game:**  
   Launch the Python file using `python main.py` (or the appropriate file name).

2. **Gameplay Basics:**  
   - Drag cards from hand to battlefield.  
   - Tap lands with right-click to generate mana.  
   - Cast spells if you have enough mana.  
   - Use the spacebar to advance turn phases.  
   - Attack and block during combat phase using mouse clicks.  
   - Activate Planeswalker abilities by clicking on them.

3. **Hotkeys:**  
   - `SPACE`: Advance phase  
   - `D`: Draw a card  
   - `E` or `ENTER`: Play the first card in hand  
   - `T`: Tap first untapped land  
   - Number keys (0–5): Add different mana types to pool  
   - `L` / `J`: Increase or decrease life  
   - `F`: Discard card  
   - `SHIFT + Left Click`: Delete card from hand or battlefield  

---

## Architecture

This project is built using Object-Oriented Programming for maintainability and scalability.

### Classes:
- **Card** – Base class for all cards  
- **Creature(Card)** – Includes combat and tap states  
- **Planeswalker(Card)** – Tracks loyalty and abilities  
- **Artifact(Card)** – Supports passive and tap-activated effects  

### Systems:
- **Effect Parser** – Converts Oracle text into effects and triggers
- **Mana System** – Parses cost strings, validates and consumes mana  
- **Combat System** – Tracks attackers, blockers, and resolves damage  
- **UI Renderer** – Displays hand, battlefield, life, mana, and animations

---

## Requirements

- Python 3.8+
- Pygame (`pip install pygame`)
- Requests (`pip install requests`)
- Or just use (`pip install -r requirements.txt`)
- Internet connection (for downloading card images via Scryfall API)
