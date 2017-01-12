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
        elif other.getRank() == self.getRank():
            wert= {'T':4, 'K':3, 'P':2, 'C':1}
            
            if wert[other.getSuit()]>wert[self.getSuit()]:
                return True
            else:
                return False
            
            
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
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
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

class metahand():
    def __init__(self, cards):
        self.cards = ()
        for instance in cards:
            self.cards += (instance,)
        
    def getCardsAsString(self):
        ku = ""
        for a in self.cards:
            ku += (" " + str(a))
        return ku
    
    def getCards(self):
        return self.cards
    
    def __str__(self):
        return str(self.getCardsAsString())
    def __repr__(self):
        return self.__str__()          

class endhand(metahand): 
    def __init__(self,type,cards):
        #types: pair,two, three, flush, straight, four, full, straightflush, royalflush
        #cards: it must be a touple
        
        self.type = type
        self.cards = ()
        for instance in cards:
            self.cards += (instance,)
        
    
    def getType(self):
        return self.type
        
    def __str__(self):
        return '%s : %s' %(self.getType(),self.getCardsAsString())
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        wert = {'pair':1,'two':2,'three':3,'straight':4,'flush':5, 'full':6,'four':7, 'straightflush':8, 'royalflush':9}
        if wert[self.getType()]<wert[other.getType()]:
            return True
        elif self.getType() == other.getType():
            if self.getType() =='pair' or self.getType() =='three':
                if self.getCards()[0]<other.getCards()[0]:
                    return True
                else:
                   return False
               
            if self.getType() =='two' or self.getType() =='full':
                if self.getCards()[-1]<other.getCards()[-1]:
                    return True
                if self.getCards()[-1]==other.getCards()[-1]:
                    if self.getCards()[0]<other.getCards()[0]:
                        return True
                    else:
                        return False
                else:
                    return False        
            if self.getType() =='straight' or self.getType() =='flush' or self.getType() =='straightflush' or self.getType() =='royalflush':    
                if self.getCards()[-1]<other.getCards()[-1]:
                    return True
                else:
                    return False
        else:
            return False
        
class possibleHand(metahand):
    def __init__(self, cards):
        self.cards = ()
        for instance in cards:
            self.cards += (instance,)
         
    
    def getCards(self):
        return self.cards
        
    def diff(self, other):
        #returns the difference between two hands and returns it as a touple
        
        #=======================================================================
        # #NOT FOR pure flushes!!!!!!
        #=======================================================================
        
        #OUTPUT when other is not flush: (number,(touple of card ranks that are missing)
        #OUTPUT when other is a flush typed straight: (number,(touple of cards that are missing)
        
        
        counter = 0
        missing = ()
        
        for othercard in other.getCards():
            checker = False
            for owncard in self.getCards():
                if othercard.getRank()==owncard.getRank():
                    checker = True
            if checker == False:
                counter += 1
                missing += (othercard,)
            return (counter,missing)
                    
    
def findhands(lysta, suits =['T', 'K', 'P', 'C'], ranks=['2','3','4', '5','6', '7', '8', '9', '10', '11', '12', '13', '14']):
    #Input: set - list of cards to evaluate
    #Output: list of hand classed objects
    lysta.sort()
    
    
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
        for k in space:
            kromka = True
            new = ()
            for kiki in k:
                for mimi in kiki:
                    if mimi in new:
                        kromka = False
                    new += (mimi,)
            if kromka != False:
                hands.append(endhand('two',new))
            
    #===========================================================================
    # # full        
    #===========================================================================
    if len(pairs)>=1 and len(threes)>=1:
        space = list(itertools.product(pairs,threes))
        for u in space:
            new = ()
            szynka = True
            for single in u:
                for duble in single:
                    if duble in new:
                        szynka = False
                    new += (duble,)
            if szynka != False:  
                hands.append(endhand('full',new)) 
    
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
        
    hands.sort()    
    return hands
    
def generateSimplified():

    lysta = []
    suits =['T', 'K', 'P', 'C']
    fu = deck()
    for a in range(51):
        lysta.append(fu.deal())
    
    #Input: set - list of cards to evaluate
    #Output: list of hand classed objects
    lysta.sort()
    
    
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
        for k in space:
            kromka = True
            new = ()
            for kiki in k:
                for mimi in kiki:
                    if mimi in new:
                        kromka = False
                    new += (mimi,)
            if kromka != False:
                hands.append(endhand('two',new))
            
    #===========================================================================
    # # full        
    #===========================================================================
    if len(pairs)>=1 and len(threes)>=1:
        space = list(itertools.product(pairs,threes))
        for u in space:
            new = ()
            szynka = True
            for single in u:
                for duble in single:
                    if duble in new:
                        szynka = False
                    new += (duble,)
            if szynka != False:  
                hands.append(endhand('full',new)) 
  
            
                        
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
        
    hands.sort()    
    return hands

allPossibleSolutions = generateSimplified()

def findPossibleHands(lysta, maxall, minus, allPossibleSolutions):
    lysta.sort()
    new = possibleHand(lysta)
    chances = {}
    
    
    for potentialhand in allPossibleSolutions:
        diff = new.diff(potentialhand)
        if diff[0] <= maxall:
            
                
            
            if potentialhand.getType() not in chances.keys():
            
                chances[potentialhand.getType()] = (diff[0]*1.0/(54-minus), diff[1])
            else:
                for elem in diff[1]:
                    if elem not in chances[potentialhand.getType()][1]:
                        old = chances[potentialhand.getType()][0]
                        lysa = chances[potentialhand.getType()][1]
                        lysa += (elem,)
                        chances[potentialhand.getType()] = (old + diff[0]*1.0/(54-minus), lysa)
    
    return chances
            

d = deck()
d.shuffle()
d.shuffle()

hand = []
for a in range(6):
    hand.append( d.deal(),)
print hand
print findPossibleHands(hand,1,6,allPossibleSolutions)


#
#kaka = {}
#for b in range(50000):
#    print 'processing %s' %(b)
#    d = deck()
#    d.shuffle()
#    d.shuffle()
#    
#    hand = []
#    for a in range(15):
#        hand.append( d.deal())
#    
#    kulka = findhands(hand)
#    if len(kulka)>0:
#        best = kulka[-1]
#        if best.getType() not in kaka.keys():
#            kaka[best.getType()]=1
#        else:
#            cizia = kaka[best.getType()]
#            kaka[best.getType()]= cizia+1
#
#print kaka
    
#d = deck()
#d.shuffle()
#d.shuffle()
#
#hand = []
#for a in range(52):
#    
#    hand.append(d.deal())
#hand.sort()
#print hand
#print len(hand)
#print len(findhands(hand))

            
    
    
    
    
