import cards

while True:
      print '//////////////////////////////////'
      print
      renka = []
      deck = cards.deck()
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
      print cards.findhands(renka)
      imput = raw_input()
      print
