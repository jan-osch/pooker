import cards
import random
import game
import math
import player

jasiek = player.userPlayer('Jasiek')
ulcia = player.userPlayer('Ulcia')

robercik = game.player('robercik')

ania = game.player('ania')

berta = game.player('berta')

joka =  game.player('joka')

peja = game.player('peja')

L = [robercik,ania,berta,joka,peja]
t = game.table(L,3000,5)
t.play()
