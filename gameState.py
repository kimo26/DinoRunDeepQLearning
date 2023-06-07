import cv2

class game_state:
    """
    Class to represent the current state of the Chrome's Dinosaur Game.
    """
    
    def __init__(self, dino, game):
        """
        Initializes the game state with the provided dinosaur and game instances.

        Args:
            dino (dino): An instance of the dino class controlling the dinosaur's actions.
            game (game): An instance of the game class controlling Chrome's Dinosaur Game.
        """
        self.dino = dino
        self.game = game

    def get(self, action,debug=False):
        """
        Performs an action, updates the game state, and calculates the reward.

        Args:
            action (int): The action to be performed. 1 corresponds to a jump.

        Returns:
            tuple: The updated game state, the reward, and a boolean indicating if the game is over.
        """
        score = self.game.getScore()
        rew = 0.1*score/10
        gameover = False
        if action == 1:
            self.dino.jump()
            rew = 0.1*score/11
        state = self.game.getScreen()
        if debug:
            cv2.imshow('game',state)
            cv2.waitKey(1)
        if self.dino.isCrashed():
            gameover = True
            rew = -10/score
            
        return state, rew, gameover
