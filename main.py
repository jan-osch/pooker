import game
import player

jasiek = player.userPlayer('Jasiek')

robercik = game.player('robercik')

ania = game.player('ania')

berta = game.player('berta')

joka =  game.player('joka')

peja = game.player('peja')

lis_of_players = [robercik, ania, berta, joka, peja, jasiek]

t = game.table(lis_of_players, 3000, 10)
t.play()
