from dino_ai import ai
from gameState import game_state as s
from dino import dino
from game import game
import argparse
import os

def main(model_name=None):
    """
    The main function that sets up and trains the AI for Chrome's Dinosaur Game.
    """

    # Ensure the model name is valid if given
    if model_name and not os.path.isfile(model_name):
        raise ValueError(f"No model file found at {model_name}")
    
    # Create game instance
    g = game()

    # Create dino instance using the game
    d = dino(g)

    # Create game state instance using the dino and game
    gs = s(d,g)

    # Create AI bot using the game and game state
    bot = ai(g,gs)

    # Train the bot
    bot.train(name=model_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train AI for Chrome Dinosaur Game.')
    parser.add_argument('-m', '--model', type=str, help='Path to the pretrained model')

    args = parser.parse_args()

    main(model_name=args.model)
