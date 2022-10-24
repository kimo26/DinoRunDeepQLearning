from dino_ai import ai
from gameState import game_state as s
from dino import dino
from game import game


g = game()
d = dino(g)
gs = s(d,g)

bot = ai(g,gs)
bot.train()


