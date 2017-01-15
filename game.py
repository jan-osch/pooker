import random

from game_round import Round

# ===============================================================================
# #STOPER - IF TRUE GAME WILL NEED ANY KEY TO CONTINIUE AFTER EACH ROUND
# ===============================================================================
debug_breaks = False


class Game:
    def __init__(self, players, pot, blinds):
        # players as a list
        # pot as int
        # blinds as int
        self.players = players
        self.pot = pot
        self.blinds = blinds
        self.originalblinds = blinds

    # ===========================================================================
    # #FINAL CHECK
    # ===========================================================================
    def perform_final_check(self):
        if len(self.get_players()) == 1:
            return True
        else:
            return False

    # ===========================================================================
    # #PLAYERS
    # ===========================================================================
    def get_players(self):
        return self.players

    def get_next_player(self, player):
        # player must be an instance of player class
        # returns next player in the self.players list
        index = self.get_players().index(player)

        if index + 1 == len(self.get_players()):
            index = -1
        return self.get_players()[index + 1]

    def update_dealers(self, removelist=[]):
        # removelist - it has to be a list of players to remove
        # FUNCTION: finds dealer and then finds next player still in game and makes him dealer
        # updates also statuses of smallblind, bigblind or smallbling & dealer

        players = self.get_players()

        # Find where dealers is, purge statuses of all players
        for player in players:
            if player.getStatus() in ('dealer', 'smallblind & dealer'):
                player.purge()
                new_dealer = self.get_next_player(player)
                while new_dealer in removelist:
                    new_dealer = self.get_next_player(new_dealer)
            else:
                player.purge()
        # if there are only 2 players dealer need to be also smallblind

        if len(players) - len(removelist) == 2:
            new_dealer.makeSmallDealer()
            newbig = self.get_next_player(new_dealer)
            # search for next player still in game
            while new_dealer in removelist:
                newbig = self.get_next_player(newbig)
            print '%s is now smallblind and dealer' % new_dealer.getName()

        # if there are more than 2 players we have smallblind bigblind and dealer
        else:
            new_dealer.makeDealer()
            newsmall = self.get_next_player(new_dealer)

            # search for next player still in game
            while newsmall in removelist:
                newsmall = self.get_next_player(newsmall)
            newsmall.makeSmallBlind()
            newbig = self.get_next_player(newsmall)

            # search for next player still in game
            while newbig in removelist:
                newbig = self.get_next_player(newbig)

            print '%s is now dealer' % new_dealer.getName()
            print '%s is now small blind' % newsmall.getName()

        newbig.makeBigBlind()
        self.sortPlayers()

        print '%s is now big blind' % newbig.getName()
        print

    def remove_player(self, player):
        # player must be an instance of player class
        # removes player from the table
        self.players.remove(player)

    def sortPlayers(self):
        # sorts players keeping their primary array
        players = self.get_players()
        head = []
        tail = []
        found = False

        for aplayer in players:
            if aplayer.getStatus() == 'normal':
                tail.append(aplayer)
            elif aplayer.getStatus() == 'dealer':
                dealerek = aplayer
                found = True
            else:

                head.append(aplayer)
        head.sort()
        for tailer in tail:
            head.append(tailer)
        if found == True:
            head.append(dealerek)
        self.players = head

    def chooseDealerAtRandom(self):
        players = self.get_players()
        randomnumber = random.randrange(len(players))
        dealer = players[randomnumber]

        dealer.makeDealer()

        small = self.get_next_player(dealer)
        small.makeSmallBlind()
        big = self.get_next_player(small)
        big.makeBigBlind()

        self.sortPlayers()
        print '%s will be first dealer' % (dealer.getName())
        print '%s will be first smallblind ' % (small.getName())
        print '%s will be first bigblind ' % (big.getName())
        print

    # ===========================================================================
    # #BLINDS
    # ===========================================================================
    def getBlinds(self):
        return self.blinds

    def raiseBlinds(self):
        old = self.getBlinds()

        self.blinds = old + self.originalblinds
        print'............................'
        print'blinds has been raised'
        print 'Smallblind is now %s, Bigblind is now %s' % (self.blinds, 2 * self.blinds)
        print '............................'
        print

    def play(self):
        # choose a dealer, smallblind and a bigblind at random
        self.chooseDealerAtRandom()

        # give players money
        for player in self.get_players():
            print '%s becomes %s chips' % (player.getName(), self.pot)
            player.addToMoney(self.pot)
        print

        # counter
        counter = 0

        while self.perform_final_check() != True:

            counter += 1

            print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
            print 'Starting round %s' % (counter)
            print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
            print

            # INITIALIZE NEW ROUND
            Round(self.get_players(), self.getBlinds()).play()

            # REMOVE PLAYERS THAT HAS RUN OUT OF CHIPS FROM THE GAME
            removelista = []
            for toremove in self.get_players():
                if toremove.getMoney() == 0 or toremove.getMoney() < 2 * self.getBlinds():
                    print
                    print 'Player %s has run out of chips and will be removed' % (toremove.getName())
                    removelista.append(toremove)

            # UPDATE DEALERS:
            # ALWAYS FIRST UPDATE DEALERS AND THEN REMOVE PLAYERS
            if len(self.get_players()) - len(removelista) > 1:
                self.update_dealers(removelista)

            # REMOVE PLAYERS:
            for andy in removelista:
                self.remove_player(andy)

            # UPDATE BLINDS:
            if counter % 4 == 0:
                self.raiseBlinds()
        print
        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        print
        print 'Game ends after %s rounds, the winner is %s' % (counter, self.get_players()[0].getName())
