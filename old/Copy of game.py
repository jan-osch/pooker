import cards
import random
import math

#===============================================================================
# #STOPER - IF TRUE GAME WILL NEED ANY KEY TO CONTINIUE AFTER EACH ROUND
#===============================================================================

keybreaks = True

class table():
    def __init__(self,players,pot, blinds):
        #players as a list
        #pot as int
        #blinds as int
        self.players = players
        self.pot = pot
        self.blinds = blinds
        self.originalblinds = blinds
        
    #===========================================================================
    # #FINAL CHECK
    #===========================================================================
    def smiesznyfinalCheck(self):
        if len(self.getPlayers()) == 1:
            return True
        else:
            return False    
    
    #===========================================================================
    # #PLAYERS
    #===========================================================================
    def getPlayers(self):
        return self.players
    
    def getNextPlayer(self, player):
        #player must be an instance of player class
        #returns next player in the self.players list
        index = self.getPlayers().index(player)
        
        if index  +1  == len(self.getPlayers()):
            index = -1
        return self.getPlayers()[index+1]
        
    def updateDealers(self, removelist = []):
        #removelist - it has to be a list of players to remove
        #FUNCTION: finds dealer and then finds next player still in game and makes him dealer
        #updates also statuses of smallblind, bigblind or smallbling & dealer
        
        players = self.getPlayers()
        
        #Find where dealers is, purge statuses of all players
        for player in players:
            if player.getStatus()in('dealer','smallblind & dealer'):
                player.purge()
                newdealer = self.getNextPlayer(player)
                while newdealer in removelist:
                    newdealer = self.getNextPlayer(newdealer)                
            else:
                player.purge()
        #if there are only 2 players dealer need to be also smallblind
                   
        if len(players)-len(removelist)==2:
            newdealer.makeSmallDealer()
            newbig = self.getNextPlayer(newdealer)
            #search for next player still in game
            while newdealer in removelist:
                newbig = self.getNextPlayer(newbig)
            print '%s is now smallblind and dealer' %newdealer.getName()
            
        #if there are more than 2 players we have smallblind bigblind and dealer
        else:
            newdealer.makeDealer()
            newsmall = self.getNextPlayer(newdealer)
            
            #search for next player still in game
            while newsmall in removelist:
                newsmall = self.getNextPlayer(newsmall)
            newsmall.makeSmallBlind()
            newbig = self.getNextPlayer(newsmall)
            
            #search for next player still in game
            while newbig in removelist:
                newbig = self.getNextPlayer(newbig)
                
            print '%s is now dealer' %newdealer.getName()
            print '%s is now small blind' %newsmall.getName()
        
        newbig.makeBigBlind()
        self.sortPlayers()    
        
        print '%s is now big blind' %newbig.getName()
        print
        
            
    
    def removePlayer(self, player):
        #player must be an instance of player class
        #removes player from the table
        self.players.remove(player)
        
    def sortPlayers(self):
        #sorts players keeping their primary array
        players = self.getPlayers()
        head = []
        tail = []
        found = False
        
        for aplayer in players:
            if aplayer.getStatus() =='normal':
                tail.append(aplayer)
            elif aplayer.getStatus() =='dealer':
                dealerek = aplayer
                found =True
            else:
                
                head.append(aplayer)
        head.sort()
        for tailer in tail:
            head.append(tailer)
        if found == True:
            head.append(dealerek)
        self.players = head
        
    
    def chooseDealerAtRandom(self):
        players = self.getPlayers()
        randomnumber = random.randrange(len(players))
        dealer = players[randomnumber]
        
        
        dealer.makeDealer()
        
        small = self.getNextPlayer(dealer)
        small.makeSmallBlind()
        big = self.getNextPlayer(small)
        big.makeBigBlind()
        
        self.sortPlayers()
        print '%s will be first dealer' %(dealer.getName())
        print '%s will be first smallblind '%(small.getName())
        print '%s will be first bigblind '%(big.getName())
        print
        
        
    #===========================================================================
    # #BLINDS
    #===========================================================================
    def getBlinds(self):
        return self.blinds
    
    def raiseBlinds(self):
        old = self.getBlinds()
        
        self.blinds = old +self.originalblinds
        print'............................'
        print'blinds has been raised'
        print 'Smallblind is now %s, Bigblind is now %s' %(self.blinds, 2*self.blinds)
        print '............................'
        print
    
    def play(self):                
        #choose a dealer, smallblind and a bigblind at random
        self.chooseDealerAtRandom()
        
        #give players money
        for player in self.getPlayers():
            print '%s becomes %s chips' %(player.getName(),self.pot)
            player.addToMoney(self.pot)
        print
        
        #counter
        counter = 0
        
        while self.smiesznyfinalCheck() != True:
                        
            counter += 1                     
            
            print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
            print 'Starting round %s' %(counter)
            print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
            print
            
            #INITIALIZE NEW ROUND
            gamestate(self.getPlayers(),self.getBlinds()).play()

                    
            #REMOVE PLAYERS THAT HAS RUN OUT OF CHIPS FROM THE GAME
            removelista = []
            for toremove in self.getPlayers():
                if toremove.getMoney() == 0 or toremove.getMoney() < 2 * self.getBlinds():
                    print
                    print 'Player %s has run out of chips and will be removed' %(toremove.getName())
                    removelista.append(toremove)
            
            #UPDATE DEALERS:
            #ALWAYS FIRST UPDATE DEALERS AND THEN REMOVE PLAYERS
            if len(self.getPlayers()) - len(removelista)  > 1:
                self.updateDealers(removelista)
                
            #REMOVE PLAYERS:
            for andy in removelista:
                self.removePlayer(andy)
                        
            #UPDATE BLINDS:
            if counter % 4 == 0 :
                self.raiseBlinds()
        print        
        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        print
        print 'Game ends after %s rounds, the winner is %s' %(counter,self.getPlayers()[0].getName())
    
     
        
class gamestate():
    
    def __init__(self, players, blinds):
        #BLINDS
        self.blinds = blinds
        #blinds as an int
        
        #PLAYERS:
        
        self.players = []
        for a in players:
            self.players.append(a)
        #players as a list
        
        
        #STATE
        self.stage = 'preflop'
        #status of the game 'preflop' 'flop' 'turn' 'river' 
        
        #DECK
        self.deck = cards.deck()
        self.cardsontable = []
        self.cardsgraveyard = []
        #cardsgraveyard will be used to store folded cards
        
        #POT / BETS
        self.pot = 0
        self.bets = {}
        self.bets['best'] = 0
        #bets will be used to store players bets
        
        #WINNERS
        self.winners = []
        #winners as a list
        
        #SPLIT POT
        self.sidelevel = 0
        self.levelpot = {}
        self.levelbets = {}
        self.levelplayers = {}
               
    
    #===========================================================================
    # #STATUS
    #===========================================================================
    def getStage(self):
        return self.stage
    #===========================================================================
    # #BETS
    #===========================================================================
    
    def addToBets(self,player,value):
        #value has to be an int
        #player must be an instance of player class        
        
        old = self.getPlayerBets(player)
        self.bets[player]=value +old
        best = self.bets['best']
        if value + old > best:
            self.bets['best'] = value + old
    
    def getBets(self):
        return self.bets 
    
    def checkBets(self):
        #returns True if every player still in round has the same amount of money in bets = best
        #else returns False
        if 'best' not in self.bets.keys():
                return False
        for player in self.getRoundPlayers():
            if self.getPlayerBetDifference(player) != 0:
                if player.getAllIn() != True:
                    return False
        return True
    
    def getPlayerBets(self,player):
        if player not in self.bets.keys():
            return 0
        else:
            return self.bets[player]
    
    def getPlayerBetDifference(self,player):
        #returns difference between player bets and the best bet so far
        if self.getPlayerBets(player) == self.bets['best']:
            return 0
        
        else:
            if self.bets['best'] - self.getPlayerBets(player) < 0:
                print self.bets['best'] - self.getPlayerBets(player)
                raise ValueError('difference smaller than 0')
            else:
                return self.bets['best'] - self.getPlayerBets(player) 
    
    def getBetsSum(self):
        sumka = 0
        for a in self.bets.keys():
            if a != 'best':
                if self.getPlayerBets(a) > 0:
                    sumka += self.getPlayerBets(a)
        return sumka
    
    def getSumPotAndBet(self):
        return self.getBetsSum() + self.getPot()    
      
    #===========================================================================
    # #ALLIN    
    #===========================================================================
    
    def getLevel(self):
        return self.sidelevel  
      
    def playAllIn(self,player,value):
        #value = value of allinbet
        #sumka - sum of money in pot        
        sumka = self.getPot()
        sumkaside = 0
        payers = []
        payers.append(player)
        best = self.getBets()['best']
        
        #iterate through every player that betted
        for aplayer in self.getBets().keys():
            if aplayer != 'best':
                payers.append(aplayer)
            
            hisbet = self.bets[aplayer]
            
            if  best <= value:
                sumka += hisbet
            else:
                if hisbet > value:
                    sumka += value
                    sumkaside += hisbet - value
                else:
                    sumka += hisbet
                    
            self.bets[aplayer] = hisbet - value
            
        self.bets['best'] = abs(best - value)
        
        self.levelpot[self.getLevel()]= sumka + value
        self.levelplayers[self.getLevel()]= payers
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
                    
    def addBetsToHighestLevel(self):
        payers = self.getRoundPlayers()
        pot = self.getPot()
        self.levelplayers[self.getLevel()]=payers
        self.levelpot[self.getLevel()]=pot    
        
    #===========================================================================
    # #POT
    #===========================================================================
    def addBetsToPot(self):
        self.addToPot(self.getBetsSum())
        self.bets = {}
        self.bets['best']=0
        
    def getPot(self):
        return self.pot    
       
    def addToPot(self,value):
        old = self.getPot()
        self.pot = old + value
    
    #===========================================================================
    # #DECK
    #===========================================================================
    def getDeck(self):
        return self.deck
    
    def deckDeal(self):
        return self.getDeck().deal()
    
    def cardsLeftInDeck(self):
        return len(self.getDeck())
    
    #===========================================================================
    # #CARDS   
    #===========================================================================
    def getCardsOnTable(self):
        return self.cardsontable
         
    def addCardToTable(self):
        self.cardsontable.append(self.deckDeal())
        self.cardsontable.sort()
    
    def burnCard(self):
        self.cardsgraveyard.append(self.deckDeal())
        
    def dealCard(self, player):
        player.addToHand(self.deckDeal())
          
    #============================================================================
    # #PLAYERS
    #============================================================================
    
    def removePlayerFromRound(self,player):
        self.players.remove(player)
    
    def getRoundPlayers(self):
        return self.players
    
    def addPlayerToWinners(self,player):
        self.winners.append(player)
    
    def getNextRoundPlayer(self, player):
        #player must be an instance of player class
        #returns next player in the self.players list
        index = self.getRoundPlayers().index(player)
        
        if index  +1  == len(self.getRoundPlayers()):
            index = -1
        return self.getRoundPlayers()[index+1]
    
    #===========================================================================
    # #BLINDS:
    #===========================================================================
    
    def getRoundBlinds(self):
        return self.blinds  
    
    #===========================================================================
    # #DISPLAY
    #===========================================================================
    def displayPlayers(self):
        for asorter in self.getRoundPlayers():
            print '%s has %s chips' %(asorter.getName(),asorter.getMoney())
        print
    
    def displayCards(self):
        print 'Cards on the Table are %s' %(self.getCardsOnTable())
    
    def displayPot(self):
        print
        if self.getLevel() ==0:
            print 'The pot is %s' %(self.getPot())
        else:
            print 'Current pot is %s' %(self.getPot())
            for a in self.levelpot.keys():
                print '%s Sidepot for %s is %s' %(a, self.levelplayers[a],self.levelpot[a])
        print
    #===========================================================================
    # #KEY BREAKS
    #===========================================================================
    def keyBreak(self):
        if keybreaks == True:
            print
            raw_input('      ***press any key to continiue***     ')
            
    #===========================================================================
    # #PLAY
    #===========================================================================
            
    def play(self):
        
        skip = False
        #=======================================================================
        # #preflop
        #=======================================================================
        self.deck.shuffle()
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print 'Preflop: '
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print
        
        self.displayPlayers()
        
        #burn a card and deal 2 cards to each player:
        self.burnCard()
        self.stage = 'preflop'
        for astarter in self.getRoundPlayers():
            self.dealCard(astarter)
            self.dealCard(astarter)
        
        #keep track of which players already taken an action    
        initialplayers = len(self.getRoundPlayers())
        stageactionlist = []
        
        #iterate through first prebets
        for netplayer in self.getRoundPlayers():
            if netplayer.getStatus() in ('smallblind','smallblind & dealer'):
                netplayer.call(self,self.getRoundBlinds())
                print
            elif netplayer.getStatus() == 'bigblind':
                netplayer.call(self,2 * self.getRoundBlinds())
                nextplayer = self.getNextRoundPlayer(netplayer)
                print
            else:
                nextplayer = self.getNextRoundPlayer(netplayer)
                netplayer.update(self)
                stageactionlist.append(netplayer)
                
                
                
        #itarate through normal actions        
        while self.checkBets() != True or len(stageactionlist) != initialplayers:                
            aplayer = nextplayer
            nextplayer = self.getNextRoundPlayer(aplayer)
            aplayer.update(self)
            if aplayer not in stageactionlist:
                stageactionlist.append(aplayer)
            
           
        #update Pot    
        self.addBetsToPot()
        
        
        #check if there are still players in game
        if len(self.getRoundPlayers()) == 1:
            self.addPlayerToWinners(self.getRoundPlayers()[0])
            skip = True
                    
        
        #skip if there is only one player left    
        if skip != True:
            
            self.keyBreak()
                   
            #=======================================================================
            # #flop
            #=======================================================================
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'Flop: '
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print
                        
            #change staus
            self.stage = 'flop'
            
            
            #burn a card and deal  3 card to table
            self.burnCard()
            self.addCardToTable()
            self.addCardToTable()
            self.addCardToTable()
                        
            #DISPLAY:
            self.displayCards()
            self.displayPot()
            self.displayPlayers()
            
            #keep track of which players already taken an action    
            initialplayers = len(self.getRoundPlayers())
            stageactionlist = []
            nextplayer = self.getRoundPlayers()[0]
            
            #iterate through first round
            while self.checkBets() != True or len(stageactionlist) != initialplayers:                
                aplayer = nextplayer
                nextplayer = self.getNextRoundPlayer(aplayer)
                aplayer.update(self)
                if aplayer not in stageactionlist:
                    stageactionlist.append(aplayer)
                
                
                      
            #update Pot
            self.addBetsToPot()   
            
            #check if there are still players in game
            if len(self.getRoundPlayers()) == 1:
                self.addPlayerToWinners(self.getRoundPlayers()[0])
                skip = True
                
        
        
        if skip != True:
            #=======================================================================
            # #turn
            #=======================================================================
            
            self.keyBreak()  
            
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'Turn: '
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print
                        
            #change staus
            self.stage = 'turn'
            
            
            #burn a card and deal  1 card to table
            self.burnCard()
            self.addCardToTable()
            
            #DISPLAY:
            self.displayCards()
            self.displayPot()
            self.displayPlayers()
                    
            #keep track of which players already taken an action    
            initialplayers = len(self.getRoundPlayers())
            stageactionlist = []
            nextplayer = self.getRoundPlayers()[0]
            
            #iterate through first round
            while self.checkBets() != True or len(stageactionlist) != initialplayers:                
                aplayer = nextplayer
                nextplayer = self.getNextRoundPlayer(aplayer)
                aplayer.update(self)
                if aplayer not in stageactionlist:
                    stageactionlist.append(aplayer)
                  
                                  
            #update Pot
            self.addBetsToPot()   
            
            #check if there are still players in game
            if len(self.getRoundPlayers()) == 1:
                self.addPlayerToWinners(self.getRoundPlayers()[0])
                skip = True
        
        #skip if there is only one player left    
        if skip != True:
            
            #=======================================================================
            # #river 
            #=======================================================================
            
            self.keyBreak()  
            
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'River: '
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print
                        
            #change staus
            self.stage = 'river'
            
            
            #burn a card and deal  1 card to table
            self.burnCard()
            self.addCardToTable()
                       
            #DISPLAY:
            self.displayCards()
            self.displayPot()
            self.displayPlayers()
                    
            #keep track of which players already taken an action    
            initialplayers = len(self.getRoundPlayers())
            stageactionlist = []
            nextplayer = self.getRoundPlayers()[0]
            
            #iterate through all players
            while self.checkBets() != True or len(stageactionlist) != initialplayers:                
                aplayer = nextplayer
                nextplayer = self.getNextRoundPlayer(aplayer)
                aplayer.update(self)
                if aplayer not in stageactionlist:
                    stageactionlist.append(aplayer)
                
                         
              
            
            #check if there are still players in game
            if len(self.getRoundPlayers()) == 1:
                self.addPlayerToWinners(self.getRoundPlayers()[0])
                skip = True
        
        #Convert system of pot into LEVLES:        
        self.addBetsToHighestLevel()   
             
        #skip if there is only one player left    
        if skip != True:
            #=======================================================================
            # #END
            #=======================================================================
            
            self.keyBreak()  
                
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'Round Evaluation: '
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print
            self.displayCards()
            self.displayPot()
            print

            #===================================================================
            # #EVALUATE HANDS
            #===================================================================
            
            #byplayer - dictionary sorting hands by player
            byplayer = {}
                        
            for aplayer in self.getRoundPlayers():
                
                #display hands and chips
                aplayer.displayHand()
                print '%s has %s chips' %(aplayer.getName(),aplayer.getMoney())
                                
                #create a sum of players hand and table cards 
                aplayerendhand = cards.listUnion(aplayer.getHand(), self.getCardsOnTable())
                
                                    
                #generate best hand of aplayer    
                endhand = cards.findhands(aplayerendhand)[-1]
                print '%s best hand is: %s' %(aplayer.getName(),endhand)
                print 
                
                #store player in byplayers dictionary
                byplayer[aplayer] = endhand                
                
                        
        #===================================================================
        # #KOMENTY ROBOCZE
        #===================================================================
        print 'levels:'
        print self.levelplayers
        print self.levelpot
        print
        
        
        #===================================================================
        # #ANALYSE LEVELS:
        #===================================================================
        for level in self.levelplayers.keys():
            
            print 'Level is %s' %(level)
            print 'Level Players are: %s' %(self.levelplayers[level])
            
            #FIND ALL HANDS AT LEVEL:
            levelhands = []
            for awinn in self.levelplayers[level]:
                levelhands.append(byplayer[awinn])
            
            #FIND BEST HAND
            levelhands.sort()
            bestatlevel = levelhands[-1]
            
            #FIND ALL PLAYERS AT LEVEL THAT HAVE THE SAME HAND:
            levelwinners = []
            for bwinn in self.levelplayers[level]:
                if byplayer[bwinn] == bestatlevel:
                    levelwinners.append(bwinn)
            
            #COMPUTE NUMBER OF WINNERS/PRIZE:
            count = len(levelwinners)
            wygrana = int(self.levelpot[level]*1.0/count)
            
            #GIVE PRIZE TO EVERY WINNER:
            for winner in levelwinners:
                winner.addToMoney(wygrana)
                if count == 1:
                    print 'Player %s won and gets %s chips' %(winner.getName(),wygrana)
                else:
                    print 'Remis: %s gets %s chips' %(winner.getName(),wygrana)                  
                        
        self.keyBreak()  
                
        print        
        print '##########################################################################'
        print 'Round ends'
        print '##########################################################################'
        print
      
class player():
    def __init__ (self,name):
        self.name = name
        self.money = 0 
        #name as a string
        #money as int
        
        #STATUS:
        self.status = 'normal'
        #status - if is blind dealer etc.
        #statuses = {'normal':3,'bigblind':2,'smallblind':1,'dealer':0, 'smallblind & dealer':1}
        
        #HAND
        self.hand = []
        #hand is always a list!
        
        #ALLIN
        self.allin = False
        
    #===========================================================================
    # #NAME
    #===========================================================================
    def getName(self):
        return self.name
    
    #===========================================================================
    # #STATUS:
    #===========================================================================
    
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
    
    #===========================================================================
    # #HAND
    #===========================================================================
    def addToHand(self, instanceofcard):
        #instanceofcard needs to be a card
        self.hand.append(instanceofcard)
        self.hand.sort()
        
    def getHand(self):
        return self.hand
    
    #===========================================================================
    # #MONEY:
    #===========================================================================
    def addToMoney(self,value):
        #value needs to be an int
        self.money = self.money + value
    def getMoney(self):
        return self.money
    def minusMoney(self,value):
        old = self.getMoney()
        self.money = old - value
    
    #===========================================================================
    # #ALLIN:
    #===========================================================================
    def getAllIn(self):
        #returns boolean if betted allin
        return self.allin        
        
    #===========================================================================
    # #ACTIONS    
    #===========================================================================
    def fold(self, gamestate):
        gamestate.removePlayerFromRound(self)
        print '%s folds' %(self.getName())
        
    def call(self, gamestate, value = None):
        
        if value == None:
            diff = gamestate.getPlayerBetDifference(self)
            if diff != 0:
                self.minusMoney(diff)
                gamestate.addToBets(self,diff)
                print '%s calls %s chips' %(self.getName(),diff)
                print '%s has %s chips left' %(self.getName(),self.getMoney())
            else:
                print '%s checks' %(self.getName())
                gamestate.addToBets(self,diff)
        else:
            gamestate.addToBets(self,value)
            self.minusMoney(value)
            print '%s calls %s chips' %(self.getName(),value)
            print '%s has %s chips left' %(self.getName(),self.getMoney())
    
    def check(self,gamestate):
        print '%s checks' %(self.getName())
        gamestate.addToBets(self,0)
                
    def bet(self,gamestate,value):
        self.minusMoney(value)
        gamestate.addToBets(self,value)
        print '%s bets %s chips' %(self.getName(),value)
        print '%s has %s chips left' %(self.getName(),self.getMoney())
    
    def Raise(self, gamestate, value):
        self.minusMoney(value)
        gamestate.addToBets(self,value)
        print '%s raises %s chips' %(self.getName(),value)
        print '%s has %s chips left' %(self.getName(),self.getMoney())
    
    def allIn(self, gamestate):
        value = self.getMoney()
        gamestate.playAllIn(self, value)
        self.minusMoney(value)
        self.allin = True
        print '%s bets all in: %s chips' %(self.getName(),value)
                
        

    #===========================================================================
    # #UPDATE:
    #===========================================================================
    def update(self,gamestate):
        
        #=======================================================================
        # #GAMESTATE ANALYSIS         
        #=======================================================================
        
        #IDENTIFY STAGE OF THE GAME      
        stage = gamestate.getStage()
        
        #IDENTIFY BLINDS:
        blinds = gamestate.getRoundBlinds()
                
        #IDENTIFY TOCALL:
        tocall = gamestate.getPlayerBetDifference(self)
        
        print '%s :' %(self.getName())
        
        folded = False
        #fold in case you don't have enough money
        if tocall > self.getMoney():
            self.fold(gamestate)
            folded = True
        
        #=======================================================================
        # #POSSIBLE GAMESTAGES:              
        #=======================================================================
        
        if not folded:
            #preflop:
            if stage == 'preflop':
                if tocall != 0:
                    self.call(gamestate)
            
            #flop
            elif stage == 'flop':
                if tocall == 0:
                    self.bet(gamestate,2*blinds)
                else:
                    self.call(gamestate)
            
            #turn
            elif stage == 'turn':
                
                if random.random() > 0.6:
                    if tocall == 0:
                        if gamestate.getPlayerBets(self)== 0:
                            self.bet(gamestate,2*blinds)
                    else:
                        self.call(gamestate)
                else:
                    sumofknowncards = cards.listUnion(self.getHand(),gamestate.getCardsOnTable())
                    
                    if len(cards.findhands(sumofknowncards)) > len(sumofknowncards):
                        if gamestate.getPlayerBets(self)== 0:
                            self.bet(gamestate,blinds + tocall)
                    else:
                        if random.random() < 0.2:
                            if tocall != 0:
                                self.fold(gamestate)
                        else:
                            self.call(gamestate)
            
            #river
            elif stage == 'river':
                if random.random() > 0.6:
                    if tocall == 0:
                        if gamestate.getPlayerBets(self)== 0:
                            self.bet(gamestate,2*blinds)
                    else:
                        self.call(gamestate)
                else:
                    sumofknowncards = cards.listUnion(self.getHand(),gamestate.getCardsOnTable())
                    
                    if len(cards.findhands(sumofknowncards)) > len(sumofknowncards):
                        if gamestate.getPlayerBets(self)== 0:
                            self.bet(gamestate,2*blinds + tocall)
                        
                    else:
                        if random.random() < 0.2:
                            if tocall != 0:
                                self.fold(gamestate)
                        else:
                            self.call(gamestate)
        
        print
                 
        
        
        
    #PURGE:
    def purge(self):
        #resets hand and resets status
        self.hand = []
        self.status = 'normal'
    
    
    #COMPARE:
    def __lt__(self, other):
        statuses = {'normal':4,'bigblind':2,'smallblind':1,'dealer':3, 'smallblind & dealer':0}
               
        if statuses[other.getStatus()] > statuses[self.getStatus()]:
            
            return True
        else:
            return False
        
    def __le__(self, other):
        statuses = {'smallblind':1, 'bigblind':2, 'normal': 3, 'dealer':4, 'smallblind & dealer':0}

        if self.getName() == other.getName():
            return True
        else:
               
            if statuses[other.getStatus()] > statuses[self.getStatus()]:
                
                return True
            else:
                return False
        
    def __eq__(self,other):
        
        if type(self) == type(other):
            if self.getName() == other.getName():
                return True
            else:
                return False
        else:
            return False 
    
    def __hash__(self): 
        return hash(id(self))
                
    
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()
    
    #DISPLAY:
    def displayHand(self):
        print '%s hand is : %s' %(self.getName(),self.getHand())
    

