from google.adk import Agent
import random

VALID_MOVES = {"rock", "paper", "scissors", "bomb"}
WIN_RULES = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock"
}

def create_initial_state():
    return {
        "round": 1,
        "max_rounds": 3,
        "user_score": 0,
        "bot_score": 0,
        "user_bomb_used": False,
        "bot_bomb_used": False,
        "history": []  # Stores per-round summaries - needed for future
    }

def validate_move(move: str, state: dict) -> dict:
    if not move:
        return {"valid": False, "move": None, "reason": "No input"}

    move = move.strip().lower()
    if move not in VALID_MOVES:
        return {"valid": False, "move": None, "reason": "Invalid move"}

    if move == "bomb" and state["user_bomb_used"]:
        return {"valid": False, "move": None, "reason": "Bomb already used"}

    return {"valid": True, "move": move, "reason": None}

def resolve_round(user_move: str, state: dict) -> dict:
    bot_moves = ["rock", "paper", "scissors"]
    if not state["bot_bomb_used"]:
        bot_moves.append("bomb")

    bot_move = random.choice(bot_moves)

    if user_move == "bomb":
        state["user_bomb_used"] = True
    if bot_move == "bomb":
        state["bot_bomb_used"] = True

    if user_move == bot_move:
        winner = "draw"
        explanation = "Both players chose the same move."
    elif user_move == "bomb":
        winner = "user"
        explanation = "Bomb beats all moves."
    elif bot_move == "bomb":
        winner = "bot"
        explanation = "Bomb beats all moves."
    else:
        if WIN_RULES[user_move] == bot_move:
            winner = "user"
            explanation = f"{user_move} beats {bot_move}."
        else:
            winner = "bot"
            explanation = f"{bot_move} beats {user_move}."

    return {
        "user_move": user_move,
        "bot_move": bot_move,
        "winner": winner,
        "explanation": explanation
    }

def update_game_state(state: dict, result: dict) -> dict:
    if result["winner"] == "user":
        state["user_score"] += 1
    elif result["winner"] == "bot":
        state["bot_score"] += 1

    state["history"].append({
        "round": state["round"],
        "user_move": result["user_move"],
        "bot_move": result["bot_move"],
        "winner": result["winner"]
    })

    state["round"] += 1
    return state

agent = Agent(
    name="RPSPlusReferee",
    description="Referee agent for Rock Paper Scissors Plus game",
    tools=[validate_move, resolve_round, update_game_state]
)

def agent_handle_turn(user_input: str, state: dict) -> dict:
    validation = validate_move(user_input, state)
    if not validation["valid"]:
        response = (
            f"Invalid move: {validation['reason']}.\n"
            "This round is wasted due to invalid input."
        )
        state["round"] += 1
        return {"state": state, "response": response}

    result = resolve_round(validation["move"], state)
    state = update_game_state(state, result)

    if result["winner"] == "user":
        outcome = "You win this round!"
    elif result["winner"] == "bot":
        outcome = "Bot wins this round!"
    else:
        outcome = "This round is a draw"

    response = (
        f"You played {result['user_move']}. "
        f"Bot played {result['bot_move']}.\n"
        f"{result['explanation']}\n"
        f"{outcome}"
    )


    return {"state": state, "response": response}

def main():
    state = create_initial_state()

    print("Welcome to Rock–Paper–Scissors–Plus!")
    print("Rules:")
    print("• Best of 3 rounds")
    print("• Moves: rock, paper, scissors, bomb (once per game)")
    print("• Bomb beats all moves")
    print("• Invalid input wastes the round\n")

    while state["round"] <= state["max_rounds"]:
        print(f"\nRound {state['round']}")
        user_input = input("Enter your move: ")

        result = agent_handle_turn(user_input, state)
        state = result["state"]

        print(result["response"])
        
    print("\n=== GAME OVER ===")
    print(f"Final Score:")
    print(f"You: {state['user_score']}")
    print(f"Bot: {state['bot_score']}")

    if state["user_score"] > state["bot_score"]:
        print("\nFinal Result: YOU WIN 🎉")
    elif state["user_score"] < state["bot_score"]:
        print("\nFinal Result: BOT WINS 🤖")
    else:
        print("\nFinal Result: DRAW 🤝")



if __name__ == "__main__":
    main()
