from dino_ai import ai
from gameState import game_state as s
from dino import dino
from game import game
import argparse
import os

def main(model_path=None):
    """
    The main function that sets up and tests the AI for Chrome's Dinosaur Game.
    """

    # Ensure model path is provided
    if not model_path:
        raise ValueError("Please provide a valid model path using --model flag.")
    
    # Ensure the model path is valid
    if not os.path.isfile(model_path):
        raise ValueError(f"No model file found at {model_path}")


    # Create game instance
    g = game()

    # Create dino instance using the game
    d = dino(g)

    # Create game state instance using the dino and game
    gs = s(d,g)

    # Create AI bot using the game and game state
    bot = ai(g,gs)

    # Test the bot with a pretrained model
    bot.test(name=model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test your AI for Chrome Dinosaur Game.')
    parser.add_argument('-m', '--model', type=str, required=True,help='Path to the pretrained model')

    args = parser.parse_args()

    main(model_name=args.model)
