
class game_state:
    
    def __init__(self, dino, game):
        self.dino = dino
        self.game = game
        
    def get(self,action):
        score = self.game.getScore()
        rew = 0.1*score/10#reward if alive
        gameover = False
        if action == 1:
            self.dino.jump()
            rew = 0.1*score/11
        state = self.game.getScreen()
        if self.dino.isCrashed():
            gameover = True
            rew = -20/score#reward when crash
            
        return state, rew,gameover
        
