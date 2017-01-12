import random
import itertools

class card:
    def __init__(self,rank, suit):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        if self.getRank() >10:
            if self.getRank() == 11:
                return str('J'+self.getSuit())
            if self.getRank()  == 12:
                return str('D'+self.getSuit())
            if self.getRank()  == 13:
                return str('K'+self.getSuit())
            if self.getRank()  == 14:
                return str('A'+self.getSuit())
            
        else:
            return str(str(self.getRank())+self.getSuit())
    def __repr__(self):
        return self.__str__()
    
    def getSuit(self):
        return self.suit
    def getRank(self):
        return self.rank
    
    def __lt__(self, other):
        if other.getRank()>self.getRank():
            return True
        else:
            return False
    def __eq__(self,other):
        if self.getRank() == other.getRank():
            return True
        else:
            return False
          

class deck:
    def __init__(self, suits =['T', 'K', 'P', 'C'], ranks=[2,3,4,5,6,7,8,9,10,11,12,13,14]):
        self.suits = suits
        self.ranks = ranks
        self.cards = []
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(card(rank,suit))
        self.shuffled = False
        
    def shuffle(self):
        for a in range(99):
            random.shuffle(self.cards)
                      
    
    def deal(self):
        return self.cards.pop(0)
   
    def __str__(self):
        k = []
        for karta in self.cards:
            k.append(str(karta))
        return str(k)
    
    def getDeck(self):
        return self.cards


class endhand(): 
    def __init__(self,typek,cards):
        #types: pair,two, three, flush, straight, four, full, straightflush, royalflush
        #cards: it must be a touple
        
        self.type = typek
        self.cards = ()
        for instance in cards:
            self.cards += (instance,)
        
    
    def getType(self):
        return self.type
    
    def getCardsAsString(self):
        
        ku = ""
        for a in self.cards:
            ku += (" " + str(a))
        return ku
    
    def getCards(self):
        return self.cards
    
    def __str__(self):
        return '%s : %s' %(self.getType(),self.getCardsAsString())
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        
        wert = {'highcard': 0,'pair':1,'two':2,'three':3,'straight':4,'flush':5, 'full':6,'four':7, 'straightflush':8, 'royalflush':9}
        if wert[self.getType()]<wert[other.getType()]:
            return True
        elif self.getType() == other.getType():
            leng = len(self.getCards())
            counter = -1
            while other.getCards()[counter].getRank() == self.getCards()[counter].getRank() and counter*-1 != leng:
                counter -= 1
            if counter *-1 == leng:
                return False
            else:
                return other.getCards()[counter].getRank() > self.getCards()[counter].getRank()     
            
        else:
            return False
        
    def __eq__(self, other):
            if type(other) == type(self):
                if self.getType() == other.getType():
                    leng = len(self.getCards())
                    counter = -1
                    while other.getCards()[counter].getRank() == self.getCards()[counter].getRank() and counter*-1 != leng:
                        counter -= 1
                    if counter *-1 == leng:
                        return True
                    else:
                        return False
                else:
                    return False
                    
            else:
                return other == self
    def __hash__(self): 
        return hash(id(self))
      
        
def listToTuple(listka): 
    c = ()
    for a in listka:
        c += (a,)
    return c

def flattenTuple(tupl):
    k = []
    for d in tupl:
        for c in d:
            k.append(c)
    k.sort()
    return listToTuple(k)
                      
    
def findhands(lysta):
    #Input: set - list of cards to evaluate
    #Output: list of hand classed objects
    lysta.sort()
    
    suits =['T', 'K', 'P', 'C']
    
    #makes two dictionaries; bysuit - cards sorted by suit, byrank - cards sorted by rank
    #bysuit/byrank[a]=(number,(touple of cards))
    #example: bysuit['T']=(4,(2T,8T,9T,KT))
    
    bysuit = {}
    byrank = {}
    
    for kind in suits:
        bysuit[kind]=(0,[])
    
    for a in range(len(lysta)):
        karta = lysta[a]
        su = karta.getSuit()
        ra = karta.getRank()
        
        
        #=======================================================================
        # #bysuit
        #=======================================================================
        asuit = bysuit[su]
        asuitlist = asuit[1]
        asuitlist.append(karta)
        bysuit[su]=(asuit[0]+1,asuitlist)
        
        
        #=======================================================================
        # #byrank
        #=======================================================================
        if ra in byrank.keys():
            arank = byrank[ra]
            aranklist = arank[1]
            aranklist.append(karta)
            byrank[ra] = (arank[0]+1,aranklist)
        else:
            byrank[ra]=(1,[karta])
    
    #sets up a collection of hands as a list:        
    hands = []
    
    #===========================================================================
    # #highcard:
    #===========================================================================
    hands.append(endhand('highcard',listToTuple(lysta)))
          
    #===========================================================================
    # #pairs,three of a kind, four of a kind 
    #===========================================================================
    #Set up a counters for pairs/ three
    pairs = []
    threes = []
    
    for ele in byrank.keys():
        
        if byrank[ele][0] >=2:
            space = list(itertools.combinations(byrank[ele][1],2))
            for g in space:
                hands.append(endhand('pair',g))
                pairs.append(g)
           
                        
        if byrank[ele][0]>=3:
            space = list(itertools.combinations(byrank[ele][1],3))
            
            for h in space:
                hands.append(endhand('three',h))
                threes.append(h)
        
                
                        
        if byrank[ele][0]==4:
            hands.append(endhand('four',byrank[ele][1]))
    
                
    #===========================================================================
    # #twopair       
    #===========================================================================
    if len(pairs)>=2:
        space = list(itertools.combinations(pairs,2))
        for v in space:
            if v[0][0].getRank() != v[1][0].getRank():
                hands.append(endhand('two',flattenTuple(v)))
            
    #===========================================================================
    # # full        
    #===========================================================================
    if len(pairs)>=1 and len(threes)>=1:
        space = list(itertools.product(pairs,threes))
        for v in space:
            if v[0][0].getRank() != v[1][0].getRank():
                hands.append(endhand('full',flattenTuple(v))) 
    
    #===========================================================================
    # #flush  
    #===========================================================================
    
    for a in bysuit.keys():
        bysuit[a][1].sort()
        numerek = bysuit[a][0]
        if numerek >=5:
            space = list(itertools.combinations(bysuit[a][1],5))
            for helo in space:
                hands.append(endhand('flush',helo))
            
                        
    #===========================================================================
    # #straight/straightflush/royalflush       
    #===========================================================================
    if len(byrank.keys())>=5:
        mainstraightspace = []
        for rank in range(2,10):
            straight = True
            lyst = []
            for helper in range(6):
                if helper + rank not in byrank.keys():
                    straight = False
                else:
                    lyst.append(byrank[helper+rank][1])
            if straight ==True:
                straightspace = list(itertools.product(lyst[0],lyst[1],lyst[2], lyst[3], lyst[4]))
                for uklad in straightspace:
                    mainstraightspace.append(uklad)
                    
                    
        #=======================================================================
        # #Kind of straight checker:            
        #=======================================================================
        for stra in mainstraightspace:
            flush = True
            last = None
            for strcard in stra:
                if strcard.getSuit() == last or last ==None:
                    last = strcard.getSuit()
                else:
                    flush = False
            if flush == True:
                
                if stra[-1].getRank()==14:
                    hands.append(endhand('royalflush',stra))
                else:
                    hands.append(endhand('straightflush',stra))
            else:         
                hands.append(endhand('straight',stra))
    
    if len(hands) != 0:
        hands.sort()    
    return hands

def listUnion(a, b):
    """ return the union of two lists """
    d = []
    for c in b:
        d.append(c)
    for g in a:
        d.append(g)
    return d
    

def checkbyrank(known,rank):
    #returns number of cards that are still unknown and could fullfill the criterium
    #known has to be a list of known cards
    counter = 4
    for kart in known:
        if kart.getRank() == rank:
            counter -= 1
    return counter

def checkbysuit(known, suit):
    #returns number of cards that are still unknown and could fullfill the criterium
    #known has to be a list of known cards
    counter = 13
    for kart in known:
        if kart.getSuit() == suit:
            counter -= 1
    return counter

def computeprobsingle(needed,aviable,leftondeck):
    #needed - number of needed cards as an int
    #aviable - number of aviable cards still in deck
    #RETURNS:
    #probability of drawing x needed of the same kind from deck
    
    if needed > aviable:
        return 0
    else:
        result = 1
        while needed >0:
            result = result *aviable*1.0/leftondeck
            aviable -= 1
            leftondeck -= 1
            needed -= 1
    return result
