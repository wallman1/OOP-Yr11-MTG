### **Detailed Commit Summary & Changelog**

#### **May 5, 2025 — Initial Setup & Exploration**
- **Initial commit:** Laid the foundational codebase for the MTG game simulator.
- Explored the capabilities of the MTG API (likely Scryfall) to understand card data retrieval.
- Started basic integration of Pygame for graphical interface.
- Implemented initial code structure, including loading cards, basic rendering, and simple interactions.

---

#### **May 12, 2025 — GUI & API Integration**
- Added GUI components for displaying cards, decks, and game info.
- Started working on image search functionalities, allowing card images to be loaded dynamically.
- Implemented keyword system to annotate cards with special abilities or traits.
- Basic setup for card effects and triggers, laying groundwork for more complex interactions.

---

#### **May 26, 2025 — Search & Deck Management**
- Developed the bulk search system to find and add multiple cards efficiently.
- Enabled saving decks to files, supporting deck building and management.
- Improved card search features, possibly with filtering or keyword tagging.
- Refined data handling for deck operations.

---

#### **May 28, 2025 — Card Search & Keyword Features**
- Integrated image search for cards, probably via Scryfall API.
- Started implementing keyword mechanics, allowing cards to have abilities like flying or trample.
- Enhanced card data parsing to include keywords and abilities.
- Improved user interface for deck creation and card selection.

---

#### **May 29, 2025 — Card Addition & Fixes**
- Fixed bugs related to adding cards to decks or game zones.
- Polished deck management features, ensuring correct card addition and removal.
- Possibly fixed issues with card data loading or image display.

---

#### **June 2, 2025 — Multiplayer & Combat**
- Added support for multiple players.
- Implemented basic combat mechanics, including attacking and blocking.
- Started refining game states and turn management.
- Fixed bugs related to player switching and turn progression.

---

#### **June 3, 2025 — Fix Tapping & Exceptions**
- Fixed bugs related to land tapping mechanics and card interactions.
- Addressed major exceptions to stabilize game flow.
- Improved tap/untap logic to handle edge cases properly.

---

#### **June 4, 2025 — Combat System Enhancements**
- Continued work on combat mechanics, possibly refining damage calculation, creature death, and effect resolution.
- Improved user interface elements related to combat.
- Enhanced game state management during combat phases.

---

#### **June 5, 2025 — Phases & Turn Progression**
- Added game phases: Untap, Draw, Main, Combat, and Resolution.
- Implemented phase transitions and automatic execution of phase-specific actions.
- Fixed bugs related to phase progression and turn switching.

---

#### **June 6, 2025 — Life Functions & Multiple Decks**
- Added functions to modify players' life totals.
- Enabled support for multiple decks per player.
- Improved deck shuffling and card drawing logic.

---

#### **June 10, 2025 — Keywords & Card Reading**
- Introduced keyword system to assign abilities like flying, trample, etc., to cards.
- Improved card reading/parsing to include keywords, abilities, and effects.
- Enhanced UI to display card traits visually.

---

#### **June 11-12, 2025 — Bug Fixes & Card Effects**
- Fixed various bugs reported earlier, including game state inconsistencies.
- Added support for card effects, triggers, and response handling.
- Polished card effects parsing, ensuring correct effect application.

---

#### **June 13, 2025 — Buffs & Tapping Mechanics**
- Implemented buff mechanics (+X/+Y) for creatures.
- Started adding tapping mechanics for lands and other permanents.
- Improved interaction with card effects related to tapping.

---

#### **June 15, 2025 — Effects Parser & Planeswalker Menu**
- Added an effects parser to interpret card text into game effects.
- Fixed bugs in effect application.
- Completed the Planeswalker menu UI, allowing players to select and activate abilities.

---

#### **June 17, 2025 — Combat System Work**
- Worked on the combat system, including attack/defense logic, damage calculation, and creature death.
- Improved the combat phase to handle more complex interactions.

---

#### **June 19, 2025 — Final Documentation & Bug Fixes**
- Completed and finalized the project documentation.
- Fixed bugs related to parsing and overall game stability.
- Moved detailed documentation into `documentation.md` for clarity.
- Ensured the entire system works cohesively, refining user interactions and game flow.