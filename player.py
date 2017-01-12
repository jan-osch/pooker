from game import *

# class that represents user controlled user
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
