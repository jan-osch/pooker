#run with PYTHONPATH set to parent diretory

import cards

while True:
    print '//////////////////////////////////'
    print
    renka = []
    deck = cards.CardDeck()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()

    for a in range(7):
        renka.append(deck.deal())
    renka.sort()
    print renka
    print cards.find_final_hands(renka)
    imput = raw_input()
    print
