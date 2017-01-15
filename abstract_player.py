class AbstractPlayer:
    def __init__(self, name):
        self.name = name
        self.money = 0
        # name as a string
        # money as int

        # STATUS:
        self.status = 'normal'
        # status - if is blind dealer etc.
        # statuses = {'normal':3,'bigblind':2,'smallblind':1,'dealer':0, 'smallblind & dealer':1}

        # HAND
        self.hand = []
        # hand is always a list!

        # ALLIN
        self.allin = False

    # ===========================================================================
    # #NAME
    # ===========================================================================
    def getName(self):
        return self.name

    # ===========================================================================
    # #STATUS:
    # ===========================================================================

    def makeDealer(self):
        self.status = 'dealer'

    def makeSmallBlind(self):
        self.status = 'smallblind'

    def makeBigBlind(self):
        self.status = 'bigblind'

    def makeSmallDealer(self):
        self.status = 'smallblind & dealer'

    def getStatus(self):
        return self.status

    # ===========================================================================
    # #HAND
    # ===========================================================================
    def addToHand(self, instanceofcard):
        # instanceofcard needs to be a card
        self.hand.append(instanceofcard)
        self.hand.sort()

    def getHand(self):
        return self.hand

    # ===========================================================================
    # #MONEY:
    # ===========================================================================
    def addToMoney(self, value):
        # value needs to be an int
        self.money = self.money + value

    def getMoney(self):
        return self.money

    def minusMoney(self, value):
        old = self.getMoney()
        self.money = old - value

    # ===========================================================================
    # #ALLIN:
    # ===========================================================================
    def getAllIn(self):
        # returns boolean if betted allin
        return self.allin

        # ===========================================================================

    # #ACTIONS
    # ===========================================================================
    def fold(self, gamestate):
        gamestate.remove_players_from_round(self)
        print '%s folds' % (self.getName())

    def call(self, gamestate, value=None):

        if value == None:
            diff = gamestate.get_player_bet_difference(self)
            if diff != 0:
                self.minusMoney(diff)
                gamestate.add_to_bets(self, diff)
                print '%s calls %s chips' % (self.getName(), diff)
                print '%s has %s chips left' % (self.getName(), self.getMoney())
            else:
                print '%s checks' % (self.getName())
                gamestate.add_to_bets(self, diff)
        else:
            gamestate.add_to_bets(self, value)
            self.minusMoney(value)
            print '%s calls %s chips' % (self.getName(), value)
            print '%s has %s chips left' % (self.getName(), self.getMoney())

    def check(self, gamestate):
        print '%s checks' % (self.getName())
        gamestate.add_to_bets(self, 0)

    def bet(self, gamestate, value):
        self.minusMoney(value)
        gamestate.add_to_bets(self, value)
        print '%s bets %s chips' % (self.getName(), value)
        print '%s has %s chips left' % (self.getName(), self.getMoney())

    def Raise(self, gamestate, value):
        self.minusMoney(value)
        gamestate.add_to_bets(self, value)
        print '%s raises %s chips' % (self.getName(), value)
        print '%s has %s chips left' % (self.getName(), self.getMoney())

    def allIn(self, gamestate):
        value = self.getMoney()
        gamestate.make_all_in_bet(self, value)
        self.minusMoney(value)
        self.allin = True
        print '%s bets all in: %s chips' % (self.getName(), value)

    # ===========================================================================
    # #UPDATE:
    # ===========================================================================
    def update(self, gamestate):
        raise NotImplementedError('Abstract method -has to be implemented')

    # PURGE:
    def purge(self):
        # resets hand and resets status
        self.hand = []
        self.status = 'normal'

    # COMPARE:
    def __lt__(self, other):
        statuses = {'normal': 4, 'bigblind': 2, 'smallblind': 1, 'dealer': 3, 'smallblind & dealer': 0}

        if statuses[other.getStatus()] > statuses[self.getStatus()]:

            return True
        else:
            return False

    def __le__(self, other):
        statuses = {'smallblind': 1, 'bigblind': 2, 'normal': 3, 'dealer': 4, 'smallblind & dealer': 0}

        if self.getName() == other.getName():
            return True
        else:
            return statuses[other.getStatus()] > statuses[self.getStatus()]

    def __eq__(self, other):
        if type(self) == type(other):
            return self.getName() == other.getName()
        else:
            return False

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    # DISPLAY:
    def displayHand(self):
        print '%s hand is : %s' % (self.getName(), self.getHand())
