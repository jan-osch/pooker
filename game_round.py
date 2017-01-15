import cards

# ===============================================================================
# #STOPER - IF TRUE GAME WILL NEED ANY KEY TO CONTINIUE AFTER EACH ROUND
# ===============================================================================
debug_breaks = False


class Round:
    def __init__(self, players, blinds):
        # BLINDS
        self.blinds = blinds
        # blinds as an int

        # PLAYERS:

        self.players = []
        for a in players:
            self.players.append(a)
        # players as a list


        # STATE
        self.stage = 'preflop'
        # status of the game 'preflop' 'flop' 'turn' 'river'

        # DECK
        self.deck = cards.CardDeck()
        self.cardsontable = []
        self.cardsgraveyard = []
        # cardsgraveyard will be used to store folded cards

        # POT / BETS
        self.pot = 0
        self.bets = {}
        self.bets['best'] = 0
        # bets will be used to store players bets

        # WINNERS
        self.winners = []
        # winners as a list

        # SPLIT POT
        self.sidelevel = 0
        self.levelpot = {}
        self.levelbets = {}
        self.levelplayers = {}

    # ===========================================================================
    # #STATUS
    # ===========================================================================
    def get_stage(self):
        return self.stage

    # ===========================================================================
    # #BETS
    # ===========================================================================

    def add_to_bets(self, player, value):
        # value has to be an int
        # player must be an instance of player class

        old = self.get_player_bets(player)
        self.bets[player] = value + old
        best = self.bets['best']
        if value + old > best:
            self.bets['best'] = value + old

    def get_bets(self):
        return self.bets

    def check_bets(self):
        # returns True if every player still in round has the same amount of money in bets = best
        # else returns False
        if 'best' not in self.bets.keys():
            return False
        for player in self.getRoundPlayers():
            if self.get_player_bet_difference(player) != 0:
                if not player.getAllIn():
                    return False
        return True

    def get_player_bets(self, player):
        if player not in self.bets.keys():
            return 0
        else:
            return self.bets[player]

    def get_player_bet_difference(self, player):
        # returns difference between player bets and the best bet so far
        if self.get_player_bets(player) == self.bets['best']:
            return 0

        else:
            if self.bets['best'] - self.get_player_bets(player) < 0:
                print self.bets['best'] - self.get_player_bets(player)
                raise ValueError('difference smaller than 0')
            else:
                return self.bets['best'] - self.get_player_bets(player)

    def get_bets_sum(self):
        sumka = 0
        for a in self.bets.keys():
            if a != 'best':
                if self.get_player_bets(a) > 0:
                    sumka += self.get_player_bets(a)
        return sumka

    def get_sum_of_pot_and_bets(self):
        return self.get_bets_sum() + self.get_pot()

        # ===========================================================================

    # #ALLIN
    # ===========================================================================

    def get_level(self):
        return self.sidelevel

    def make_all_in_bet(self, player, value):
        # value = value of allinbet
        # sumka - sum of money in pot
        sumka = self.get_pot()
        sumkaside = 0
        payers = []
        payers.append(player)
        best = self.get_bets()['best']

        # iterate through every player that betted
        for aplayer in self.get_bets().keys():
            if aplayer != 'best':
                payers.append(aplayer)

            hisbet = self.bets[aplayer]

            if best <= value:
                sumka += hisbet
            else:
                if hisbet > value:
                    sumka += value
                    sumkaside += hisbet - value
                else:
                    sumka += hisbet

            self.bets[aplayer] = hisbet - value

        self.bets['best'] = abs(best - value)

        self.levelpot[self.get_level()] = sumka + value
        self.levelplayers[self.get_level()] = payers
        self.sidelevel += 1
        self.pot = sumkaside

        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        print 'players'
        print self.levelplayers
        print 'level pot'
        print self.levelpot
        print 'new pot'
        print self.pot
        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    def add_bets_to_highest_level(self):
        payers = self.getRoundPlayers()
        pot = self.get_pot()
        self.levelplayers[self.get_level()] = payers
        self.levelpot[self.get_level()] = pot

        # ===========================================================================

    # #POT
    # ===========================================================================
    def add_bets_to_pot(self):
        self.add_to_pot(self.get_bets_sum())
        self.bets = {'best': 0}

    def get_pot(self):
        return self.pot

    def add_to_pot(self, value):
        old = self.get_pot()
        self.pot = old + value

    # ===========================================================================
    # #DECK
    # ===========================================================================
    def get_deck(self):
        return self.deck

    def deal_card_from_deck(self):
        return self.get_deck().deal()

    # ===========================================================================
    # #CARDS
    # ===========================================================================
    def get_cards_on_table(self):
        return self.cardsontable

    def add_card_to_table(self):
        self.cardsontable.append(self.deal_card_from_deck())
        self.cardsontable.sort()

    def burn_card(self):
        self.cardsgraveyard.append(self.deal_card_from_deck())

    def deal_card_to_player(self, player):
        player.addToHand(self.deal_card_from_deck())

    # ============================================================================
    # #PLAYERS
    # ============================================================================

    def remove_players_from_round(self, player):
        self.players.remove(player)

    def getRoundPlayers(self):
        return self.players

    def addPlayerToWinners(self, player):
        self.winners.append(player)

    def getNextRoundPlayer(self, player):
        # player must be an instance of player class
        # returns next player in the self.players list
        index = self.getRoundPlayers().index(player)

        if index + 1 == len(self.getRoundPlayers()):
            index = -1
        return self.getRoundPlayers()[index + 1]

    # ===========================================================================
    # #BLINDS:
    # ===========================================================================

    def getRoundBlinds(self):
        return self.blinds

        # ===========================================================================

    # #DISPLAY
    # ===========================================================================
    def displayPlayers(self):
        for asorter in self.getRoundPlayers():
            print '%s has %s chips' % (asorter.getName(), asorter.getMoney())
        print

    def displayCards(self):
        print 'Cards on the Table are %s' % (self.get_cards_on_table())

    def displayPot(self):
        print
        if self.get_level() == 0:
            print 'The pot is %s' % (self.get_pot())
        else:
            print 'Current pot is %s' % (self.get_pot())
            for a in self.levelpot.keys():
                print '%s Sidepot for %s is %s' % (a, self.levelplayers[a], self.levelpot[a])
        print

    # ===========================================================================
    # #KEY BREAKS
    # ===========================================================================
    def keyBreak(self):
        if debug_breaks == True:
            print
            raw_input('      ***press any key to continiue***     ')

    # ===========================================================================
    # #PLAY
    # ===========================================================================

    def play(self):

        skip = False
        # =======================================================================
        # #preflop
        # =======================================================================
        self.deck.shuffle()
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print 'Preflop: '
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print

        self.displayPlayers()

        # burn a card and deal 2 cards to each player:
        self.burn_card()
        self.stage = 'preflop'
        for astarter in self.getRoundPlayers():
            self.deal_card_to_player(astarter)
            self.deal_card_to_player(astarter)

        # keep track of which players already taken an action
        initialplayers = len(self.getRoundPlayers())
        stageactionlist = []

        # iterate through first prebets
        for netplayer in self.getRoundPlayers():
            if netplayer.getStatus() in ('smallblind', 'smallblind & dealer'):
                netplayer.call(self, self.getRoundBlinds())
                print
            elif netplayer.getStatus() == 'bigblind':
                netplayer.call(self, 2 * self.getRoundBlinds())
                nextplayer = self.getNextRoundPlayer(netplayer)
                print
            else:
                nextplayer = self.getNextRoundPlayer(netplayer)
                netplayer.update(self)
                stageactionlist.append(netplayer)

        # itarate through normal actions
        while self.check_bets() != True or len(stageactionlist) != initialplayers:
            aplayer = nextplayer
            nextplayer = self.getNextRoundPlayer(aplayer)
            aplayer.update(self)
            if aplayer not in stageactionlist:
                stageactionlist.append(aplayer)

        # update Pot
        self.add_bets_to_pot()

        # check if there are still players in game
        if len(self.getRoundPlayers()) == 1:
            self.addPlayerToWinners(self.getRoundPlayers()[0])
            skip = True

        # skip if there is only one player left
        if skip != True:

            self.keyBreak()

            # =======================================================================
            # #flop
            # =======================================================================
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'Flop: '
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print

            # change staus
            self.stage = 'flop'

            # burn a card and deal  3 card to table
            self.burn_card()
            self.add_card_to_table()
            self.add_card_to_table()
            self.add_card_to_table()

            # DISPLAY:
            self.displayCards()
            self.displayPot()
            self.displayPlayers()

            # keep track of which players already taken an action
            initialplayers = len(self.getRoundPlayers())
            stageactionlist = []
            nextplayer = self.getRoundPlayers()[0]

            # iterate through first round
            while self.check_bets() != True or len(stageactionlist) != initialplayers:
                aplayer = nextplayer
                nextplayer = self.getNextRoundPlayer(aplayer)
                aplayer.update(self)
                if aplayer not in stageactionlist:
                    stageactionlist.append(aplayer)

            # update Pot
            self.add_bets_to_pot()

            # check if there are still players in game
            if len(self.getRoundPlayers()) == 1:
                self.addPlayerToWinners(self.getRoundPlayers()[0])
                skip = True

        if skip != True:
            # =======================================================================
            # #turn
            # =======================================================================

            self.keyBreak()

            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'Turn: '
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print

            # change staus
            self.stage = 'turn'

            # burn a card and deal  1 card to table
            self.burn_card()
            self.add_card_to_table()

            # DISPLAY:
            self.displayCards()
            self.displayPot()
            self.displayPlayers()

            # keep track of which players already taken an action
            initialplayers = len(self.getRoundPlayers())
            stageactionlist = []
            nextplayer = self.getRoundPlayers()[0]

            # iterate through first round
            while self.check_bets() != True or len(stageactionlist) != initialplayers:
                aplayer = nextplayer
                nextplayer = self.getNextRoundPlayer(aplayer)
                aplayer.update(self)
                if aplayer not in stageactionlist:
                    stageactionlist.append(aplayer)

            # update Pot
            self.add_bets_to_pot()

            # check if there are still players in game
            if len(self.getRoundPlayers()) == 1:
                self.addPlayerToWinners(self.getRoundPlayers()[0])
                skip = True

        # skip if there is only one player left
        if skip != True:

            # =======================================================================
            # #river
            # =======================================================================

            self.keyBreak()

            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'River: '
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print

            # change staus
            self.stage = 'river'

            # burn a card and deal  1 card to table
            self.burn_card()
            self.add_card_to_table()

            # DISPLAY:
            self.displayCards()
            self.displayPot()
            self.displayPlayers()

            # keep track of which players already taken an action
            initialplayers = len(self.getRoundPlayers())
            stageactionlist = []
            nextplayer = self.getRoundPlayers()[0]

            # iterate through all players
            while self.check_bets() != True or len(stageactionlist) != initialplayers:
                aplayer = nextplayer
                nextplayer = self.getNextRoundPlayer(aplayer)
                aplayer.update(self)
                if aplayer not in stageactionlist:
                    stageactionlist.append(aplayer)

            # check if there are still players in game
            if len(self.getRoundPlayers()) == 1:
                self.addPlayerToWinners(self.getRoundPlayers()[0])
                skip = True

        # Convert system of pot into LEVLES:
        self.add_bets_to_highest_level()

        # =======================================================================
        # #END
        # =======================================================================

        self.keyBreak()

        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print 'Round Evaluation: '
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print
        self.displayCards()
        self.displayPot()
        print self.getRoundPlayers()
        print

        # ===================================================================
        # #EVALUATE HANDS
        # ===================================================================

        # byplayer - dictionary sorting hands by player
        byplayer = {}

        for aplayer in self.getRoundPlayers():
            # display hands and chips
            aplayer.displayHand()
            print '%s has %s chips' % (aplayer.getName(), aplayer.getMoney())

            # create a sum of players hand and table cards
            aplayerendhand = cards.listUnion(aplayer.getHand(), self.get_cards_on_table())

            # generate best hand of aplayer
            endhand = cards.find_final_hands(aplayerendhand)[-1]
            print '%s best hand is: %s' % (aplayer.getName(), endhand)
            print

            # store player in byplayers dictionary
            byplayer[aplayer] = endhand

        # ===================================================================
        # #KOMENTY ROBOCZE
        # ===================================================================
        print 'levels:'
        print self.levelplayers
        print self.levelpot
        print

        # ===================================================================
        # #ANALYSE LEVELS:
        # ===================================================================

        for level in self.levelplayers.keys():

            print 'Level is %s' % (level)
            print 'Level Players are: %s' % (self.levelplayers[level])

            # FIND ALL HANDS AT LEVEL:
            levelhands = []
            for awinn in self.levelplayers[level]:
                if awinn in self.getRoundPlayers():
                    levelhands.append(byplayer[awinn])

            # FIND BEST HAND
            levelhands.sort()
            bestatlevel = levelhands[-1]

            # FIND ALL PLAYERS AT LEVEL THAT HAVE THE SAME HAND:
            levelwinners = []
            for bwinn in self.levelplayers[level]:
                if byplayer[bwinn] == bestatlevel:
                    levelwinners.append(bwinn)

            # COMPUTE NUMBER OF WINNERS/PRIZE:
            count = len(levelwinners)
            wygrana = int(self.levelpot[level] * 1.0 / count)

            # GIVE PRIZE TO EVERY WINNER:
            for winner in levelwinners:
                winner.addToMoney(wygrana)
                if count == 1:
                    print 'Player %s won and gets %s chips' % (winner.getName(), wygrana)
                else:
                    print 'Remis: %s gets %s chips' % (winner.getName(), wygrana)

        self.keyBreak()

        print
        print '##########################################################################'
        print 'Round ends'
        print '##########################################################################'
        print
