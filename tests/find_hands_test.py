#run with PYTHONPATH set to parent diretory

import cards

L = [cards.Card(2, 'T'), cards.Card(3, 'T'), cards.Card(3, 'K')]

print cards.find_final_hands(L)
