from time import sleep

#sprite character
class dino:
    def __init__(self,game):
        self.game = game
        self.jump()#start game
        sleep(0.25)#keep otherwise error will occur
    def jump(self):
        self.game.up()
    '''
    def duck(self):
        self.game.down()
    def isRunning(self):
        return self.game.isPlaying()
    '''
    def isCrashed(self):
        return self.game.isCrashed()
