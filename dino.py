from time import sleep

class dino:
    """
    Class to interact with the Chrome Dino (Sprite)
    """

    def __init__(self, game):
        """
        Initializes the dinosaur with the provided game instance and makes the dinosaur jump.

        Args:
            game (game): An instance of the game class controlling Chrome's Dinosaur Game.
        """
        self.game = game
        self.jump()
        sleep(0.2)

    def jump(self):
        """
        Makes the dinosaur jump by calling the game's up method.
        """
        self.game.up()

    def isCrashed(self):
        """
        Checks if the dinosaur has crashed by calling the game's isCrashed method.

        Returns:
            bool: True if the dinosaur has crashed, False otherwise.
        """
        return self.game.isCrashed()
