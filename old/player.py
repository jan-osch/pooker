from game import *


class userPlayer(player):
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
#        
#    #===========================================================================
#    # #NAME
#    #===========================================================================
#    def getName(self):
#        return self.name
#    
#    #===========================================================================
#    # #STATUS:
#    #===========================================================================
#    
#    def makeDealer(self):
#        self.status = 'dealer'
#    def makeSmallBlind(self):
#        self.status = 'smallblind'
#    def makeBigBlind(self):
#        self.status = 'bigblind'
#    def makeSmallDealer(self):
#        self.status = 'smallblind & dealer'
#    def getStatus(self):
#        return self.status
#    
#    #===========================================================================
#    # #HAND
#    #===========================================================================
#    def addToHand(self, instanceofcard):
#        #instanceofcard needs to be a card
#        self.hand.append(instanceofcard)
#        self.hand.sort()
#        
#    def getHand(self):
#        return self.hand
#    
#    #===========================================================================
#    # #MONEY:
#    #===========================================================================
#    def addToMoney(self,value):
#        #value needs to be an int
#        self.money = self.money + value
#    def getMoney(self):
#        return self.money
#    def minusMoney(self,value):
#        old = self.getMoney()
#        self.money = old - value
#    
#    #===========================================================================
#    # #ALLIN:
#    #===========================================================================
#    def getAllIn(self):
#        #returns boolean if betted allin
#        return self.allin        
#        
#    #===========================================================================
#    # #ACTIONS    
#    #===========================================================================
#    def fold(self, gamestate):
#        gamestate.removePlayerFromRound(self)
#        print '%s folds' %(self.getName())
#        
#    def call(self, gamestate, value = None):
#        
#        if value == None:
#            diff = gamestate.getPlayerBetDifference(self)
#            if diff != 0:
#                self.minusMoney(diff)
#                gamestate.addToBets(self,diff)
#                print '%s calls %s chips' %(self.getName(),diff)
#                print '%s has %s chips left' %(self.getName(),self.getMoney())
#            else:
#                print '%s checks' %(self.getName())
#                gamestate.addToBets(self,diff)
#        else:
#            gamestate.addToBets(self,value)
#            self.minusMoney(value)
#            print '%s calls %s chips' %(self.getName(),value)
#            print '%s has %s chips left' %(self.getName(),self.getMoney())
#    
#    def check(self,gamestate):
#        print '%s checks' %(self.getName())
#        gamestate.addToBets(self,0)
#                
#    def bet(self,gamestate,value):
#        self.minusMoney(value)
#        gamestate.addToBets(self,value)
#        print '%s bets %s chips' %(self.getName(),value)
#        print '%s has %s chips left' %(self.getName(),self.getMoney())
#    
#    def Raise(self, gamestate, value):
#        self.minusMoney(value)
#        gamestate.addToBets(self,value)
#        print '%s raises %s chips' %(self.getName(),value)
#        print '%s has %s chips left' %(self.getName(),self.getMoney())
#    
#    def allIn(self, gamestate):
#        value = self.getMoney()
#        gamestate.playAllIn(self, value)
#        self.minusMoney(value)
#        self.allin = True
#        print '%s bets all in: %s chips' %(self.getName(),value)
#    #PURGE:
#    def purge(self):
#        #resets hand and resets status
#        self.hand = []
#        self.status = 'normal'
#    
#    
#    #COMPARE:
#    def __lt__(self, other):
#        statuses = {'normal':4,'bigblind':2,'smallblind':1,'dealer':3, 'smallblind & dealer':0}
#               
#        if statuses[other.getStatus()] > statuses[self.getStatus()]:
#            
#            return True
#        else:
#            return False
#        
#    def __le__(self, other):
#        statuses = {'smallblind':1, 'bigblind':2, 'normal': 3, 'dealer':4, 'smallblind & dealer':0}
#
#        if self.getName() == other.getName():
#            return True
#        else:
#               
#            if statuses[other.getStatus()] > statuses[self.getStatus()]:
#                
#                return True
#            else:
#                return False
#        
#    def __eq__(self,other):
#        
#        if type(self) == type(other):
#            if self.getName() == other.getName():
#                return True
#            else:
#                return False
#        else:
#            return False 
#    
#    def __hash__(self): 
#        return hash(id(self))
#                
#    
#    def __str__(self):
#        return str(self.name)
#    
#    def __repr__(self):
#        return self.__str__()
#    
#    #DISPLAY:
#    def displayHand(self):
#        print '%s hand is : %s' %(self.getName(),self.getHand())
    

    #===========================================================================
    # #UPDATE:
    #===========================================================================
    def update(self,gamestate):
        
        #=======================================================================
        # #GAMESTATE ANALYSIS         
        #=======================================================================
                
        #MONEY:
        money = self.getMoney()
                        
        #IDENTIFY TOCALL:
        tocall = gamestate.getPlayerBetDifference(self)
        if not self.allin:
            print'////////////////////////////////'
            print '%s :' %(self.getName())
            print
            if gamestate.getCardsOnTable() != []:
                print gamestate.displayCards()
            print 'Your hand is %s'%(self.getHand())
            print '%s has to call %s'%(self.getName(), tocall)
            print
            
            
            #POSSIBLE ACTIONS:
            if tocall == 0:
                possibleactions = 'Fold, Check, Bet, Allin'
                act = ['F','H','B', 'A']
            elif tocall < money:
                possibleactions = 'Fold, Call, Raise, Allin'
                act = ['F', 'C', 'R', 'A']
            elif tocall >= money:
                possibleactions = 'Fold, Allin'
                act = ['F', 'A']
                
                
                
            print 'Possible actions are: %s' %(possibleactions)
            print 'Press F to Fold, H to check, C to call, B to bet, R to raise, A to bet Allin'
            print
            imput = raw_input('Please choose an action: ')
            print
            
            while imput not in act:
                print 'Selcted wrong key:'
                imput = raw_input('Please choose an action: ')
            
            if imput == 'F':
                self.fold(gamestate)
            
            elif imput == 'H':
                self.check(gamestate)
            
            elif imput == 'C':
                self.call(gamestate)
            
            elif imput == 'A':
                self.allIn(gamestate)
            
            elif imput == 'R':
                maxa = money - tocall
                print 'Maximum of raise is %s' %(maxa)
                valuee = raw_input('please imput a value')
                valuee = int(valuee)
                while valuee > maxa:
                    valuee = raw_input('please imput a value')
                    valuee = int(valuee)
                
                if valuee == maxa:
                    self.allIn(gamestate)
                else:
                    self.bet(gamestate,tocall + valuee)
            
            elif imput == 'B':
                maxa = money
                print 'Maximum of bet is %s' %(maxa)
                valuee = raw_input('please imput a value')
                valuee = int(valuee)
                while valuee > maxa:
                    valuee = raw_input('please imput a value')
                    valuee = int(valuee)
                
                if valuee == maxa:
                    self.allIn(gamestate)
                else:
                    self.bet(gamestate,tocall + valuee) 
                
            print'////////////////////////////////'
            print
        
        
        
        
         
        
        
        
   
