Rock–Paper–Scissors (Google ADK)

This project implements a CLI-based conversational game called "Rock–Paper–Scissors", where a bot acts as a "referee" using Google Agent Development Kit (ADK).

The bot validates user input, decides round outcomes based on game rules, tracks scores across rounds and automatically ends the game with a clear final result.

---------------------------------------------------------------------------------------
* Game Rules

- Best of 3 rounds
- Valid moves:
  - `rock`
  - `paper`
  - `scissors`
  - `bomb` (can be used only once per game)
- Bomb beats all other moves
- Invalid input wastes the round

----------------------------------------------------------------------------------------
* Design Overview

- The bot is implemented as a Google ADK Agent.
- The agent acts as a referee, not a player
- All game logic is implemented using explicit tools (functions).
- Game state is maintained outside the agent and passed between turns

This design keeps the system deterministic, predictable and rule-safe.

-----------------------------------------------------------------------------------------
* Tools Used by the Agent

The agent orchestrates the following tools:

- `validate_move`  
  Validates and normalizes user input

- `resolve_round`  
  Determines the bot’s move and the round outcome

- `update_game_state`  
  Updates score, round count, and game history

-----------------------------------------------------------------------------------------
* Game Flow

1. Bot explains the rules (≤ 5 lines)
2. Bot prompts the user for a move
3. User input is validated
4. Bot decides and explains the round outcome
5. Round count and scores are updated
6. After 3 rounds, the game ends automatically with:
   - Final scores
   - Winner / draw declaration

--------------------------------------------------------------------------------------
* How to Run

1. Install dependencies
```bash
pip install google-adk
