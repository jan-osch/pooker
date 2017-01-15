from game import Game
from bot_player import BotPlayer
from user_player import UserPlayer

jasiek = UserPlayer('Jasiek')

robercik = BotPlayer('robercik')

ania = BotPlayer('ania')

berta = BotPlayer('berta')

joka = BotPlayer('joka')

peja = BotPlayer('peja')

lis_of_players = [robercik, ania, berta, joka, peja]

t = Game(lis_of_players, 3000, 10)
t.play()
