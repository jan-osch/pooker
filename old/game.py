import random

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
    
    def getSuit(self):
        return self.suit
    def getRank(self):
        return self.rank
    
    def __lt__(self, other):
        if other.getRank()>self.getRank():
            return True
        else:
            return False
        
    
class table:
    def __init__(self):
        return None
    
class player:
    def __init__(self):
        return None

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
        leng = len(self.cards)
        for a in range(leng):
            ran = a
            while ran == a:
                ran = random.randrange(0,leng) 
            old = self.cards[ran]
            new = self.cards[a]
            self.cards[ran]=new
            self.cards[a]=old
        self.shuffled = True        
           
    
    def deal(self):
        return self.cards.pop(0)
   
    def __str__(self):
        k = []
        for karta in self.cards:
            k.append(str(karta))
        return str(k)
    
    def getDeck(self):
        return self.cards
        
    
d = deck()
d.shuffle()
hand =[]

for a in range(7):
    hand.append(d.deal())
    
for a in hand:
    print '***'
    print a
    print a.getSuit()
    print a.getRank()

print 
print    

class endhand(): 
    def __init__(self,type,cards):
        #types: pair,two, three, flush, straight, four, straightflush, royalflush
        #cards: it must be a touple
        
        self.type = type
        self.cards = cards
        
    def getCards(self):
        return self.cards
    def getType(self):
        return self.type
    def getCardsAsString(self):
        ku = ""
        for a in self.cards:
            ku += (" " + str(a))
        return ku
    
    def __str__(self):
        return '%S : %S' %(self.getType(),self.getCardsAsString())
        

    
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
        bysuit[kind]=(0,())
        
    
    
    for a in range(len(lysta)):
        karta = lysta[a]
        
        su = karta.getSuit()
        ra = karta.getRank()
        
        oldnu = bysuit[su][0]
        oldly= bysuit[su][1]
        oldly += (karta,)
        
        bysuit[su]=(oldnu+1,oldly)
        
        if ra in byrank.keys():
            kupka = byrank[ra]
            klocek = kupka[1] + (karta,)
            byrank[ra] = (kupka[0]+1,klocek)
        else:
            byrank[ra]=(1,(karta))
    
    #sets up a collection of hands as a list:        
    hands = []
    
    #===========================================================================
    # #pairs,three of a kind, four of a kind 
    #===========================================================================
    #Set up a counters for pairs/ three
    for ele in byrank.keys():
        
        if byrank[ele][0]==2:
            hand.append(endhand('pair',byrank[ele][1]))
                        
                        
        if byrank[ele][0]==3:
            hand.append(endhand('three',byrank[ele][1]))
                        
        if byrank[ele][0]==4:
            hand.append(endhand('four',byrank[ele][1]))
    
    #===========================================================================
    # #flush  
    #===========================================================================
    
    for a in bysuit.keys():
        bysuit[a][1].sort()
        numerek = bysuit[a][0]
        if numerek >=5:
            if numerek == 5:
                hands.append(endhand('flush'),bysuit[a][1])
            else:
                for b in range(numerek - 4):
                    new = ()
                    for c in range(5):
                        new += (bysuit[a][1][c+b],)
                    hands.append(endhand('flush'),new)
                        
    #===========================================================================
    # #straight/straightflush/royalflush       
    #===========================================================================
    if len(byrank.keys())>=5:
        byglyst = []
        for rank in range(2,10):
            straight = True
            lyst = ()
            for helper in range(6):
                if helper + rank not in byrank.keys():
                    straight = False
                else:
                    lyst += (byrank[helper+rank],)
            if straight ==True:
                byglyst.append(lyst)
        
        for a in byglyst:
            flush = True
            last = None
            for b in a:
                if b.getsuit() != last or last ==None:
                    last = b.getsuit()
                else:
                    flush = False
            if flush == True:
                a.sort()
                if a[-1].getrank()==14:
                    hands.append(endhand('royalflush',a))
                else:
                    hands.append(endhand('straightflush',a))
            else:         
                hands.append(endhand('straight',a))
        
                

    return hands
     
findhands(hand)
            
    
    
    
    
