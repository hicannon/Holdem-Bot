from random import shuffle
class Card:
    #0=Spades (b), 1=heart (r), 2=diamond (r), 3=club (b)
    def __init__(self, num, suit):
        self.num = num;
        self.suit = suit;
    def getStringOfSuit(self, suit):
        if suit==0:
            return "Spades"
        elif suit==1:
            return "Hearts"
        elif suit==2:
            return "Diamond"
        elif suit==3:
            return "Club"
        else:
            return "Bad suit"
    def __eq__(self, other):
        return (self.num==other.num and self.suit==other.suit)
    def __str__(self):
        return str(self.num) + " of " + self.getStringOfSuit(self.suit)
    def __repr__(self):
        return self.__str__()
class Player:
    def __init__(self, playerNum, cash):
        self.playerNum = playerNum
        self.cards = ()
        self.cash = cash
        
class Holdem:
    #stage: 0=preflop, 1=flop, 2=turn, 3=river
    def __init__(self, lowLimit, highLimit, startCash):
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        self.roundNum = 0
        self.stage = 0
        self.players = [Player(0, startCash), Player(1, startCash)]
        self.deck = self.genDeck()
        self.hasDelt = False
        self.turn = True #true for player A and false for player B
        self.table=[]
        self.pot = 0;
    def genDeck(self):
        deck = []
        for num in range(13):
            for suit in range (4):
                deck.append(Card(num+1, suit))
        shuffle(deck)
        return deck
    def deal(self):
        if self.hasDelt:
            print "DEBUG: Deal called twice in a round"
            return
        if self.stage==0: #preflop
            for player in self.players:
                player.cards = (self.deck.pop(), self.deck.pop())
            print "Player one's hand: "
            print self.players[0].cards
            print "Player two's hand: "
            print self.players[1].cards
        elif self.stage==1: #flop
            self.table.append(self.deck.pop())
            self.table.append(self.deck.pop())
            self.table.append(self.deck.pop())
            print "Flop: "
            print self.table
        elif self.stage==2: #turn
            self.table.append(self.deck.pop())
            print "Turn: "
            print self.table
        elif self.stage==3: #turn
            self.table.append(self.deck.pop())
            print "River: "
            print self.table
        self.hasDelt = True
    def checkWinner(self):
        #Do checks
        self.__endRound__()
        pass
    def playerCheck(self, playerNum):
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        if self.stage ==4:
            self.checkWinner()
        self.__endStage__()
    def playerRaise(self, playerNum):
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        if self.players[playerNum].cash < self.highLimit:
            print "DEBUG: Not enough cash!"
            return
        self.players[playerNum].cash -= self.highLimit
        self.pot = self.highLimit
        self.turn = not self.turn
    def playerFold(self, playerNum):
        if self.turn!=playerNum:
            print "DEBUG: Not this player's turn"
            return
        self.checkWinner()
    #you should not call these functions
    def __endRound__(self):
        self.hasDelt = False
        self.stage = 0
        self.pot = 0
        self.table = []
        self.deck = self.genDeck()
    def __endStage__(self):
        self.hasDelt = False
        self.stage+=1
        self.stage%=4;