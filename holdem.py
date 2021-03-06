import random
from random import shuffle
from copy import deepcopy
import itertools
class Card:
	#0=Spades (b), 1=heart (r), 2=diamond (r), 3=club (b)
	def __init__(self, num, suit):
		self.num = num;
		self.suit = suit;
	def card_to_number(self):
	#so that one card correspnd to the index in the one-dim array of length 52
		if self.num != 14:
			return self.num + self.suit * 13 -1
		if self.num == 14:
			return 1+ self.suit*13 -1
	def num_to_card(self,num):
		suit = num/13
		b = num%13
		if b==0:
			b=14
		else:
			b+=1
		return Card(b,suit)
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
	
	def getCharOfSuit(self, suit):
		if suit==0:
			return "S"
		elif suit==1:
			return "H"
		elif suit==2:
			return "D"
		elif suit==3:
			return "C"
		else:
			return "Bad suit"
	def getSuitOfChar(self,suit):
		suit = suit.lower()
		if suit=='s':
			return 0
		elif suit=='h':
			return 1
		elif suit=='d':
			return 2
		elif suit=='c':
			return 3
		else:
			return -1;

	def getCardOfNumA(self,num):
		if num==11:
			return 'J'
		elif num==12:
			return 'Q'
		elif num==13:
			return 'K'
		elif num==14:
			return 'A'
		elif num==10:
		    return 'T'
		else:
			return str(num)	
		
	def getCardOfNum(self, num):
		if num==14:
			return '1'
		elif num==11:
			return 'J'
		elif num==12:
			return 'Q'
		elif num==13:
			return 'K'
		elif num==14:
			return 'A'
		#elif num==10:
		#    return 'T'
		else:
			return str(num)
	def __eq__(self, other):
		return (self.num==other.num and self.suit==other.suit)
	def __str__(self):
		return str(self.num) + " of " + self.getStringOfSuit(self.suit)
	def __repr__(self):
		return repr((self.num, self.suit))
class Player:
	def __init__(self, playerNum, cash, name=""):
		self.playerNum = playerNum
		self.cards = ()
		self.cash = cash
		self.name = name
		
class Holdem:
	#stage: 0=preflop, 1=flop, 2=turn, 3=river, 4=end
	def __init__(self, lowLimit, highLimit, numRaisesAllowed = 4, debug=False, manual=False):
		self.debug = debug;
		self.lowLimit = lowLimit
		self.highLimit = highLimit
		self.numRaisesAllowed = numRaisesAllowed;
		self.raisesCurrentRound = 0
		self.betCurrentRound = [0,0]
		self.roundNum = 0
		self.stage = 0
		self.players = [Player(0, 0), Player(1, 0)]
		self.deck = self.genDeck()
		self.hasDelt = False
		self.turn = True #true for player A and false for player B
		self.table=[]
		self.pot = 0
		self.dealer = 1
		self.actionRequired = 2
		self.betCurrentRound[not self.dealer] = self.lowLimit
		self.betCurrentRound[self.dealer] = self.lowLimit/2.0
		self.deal(debug, manual)
		self.callBacks = []
		self.manual = manual
		self.stats = [{"Check": 1, "Call": 1, "Raise": 1, "Fold": 1},{"Check": 1, "Call": 1, "Raise": 1, "Fold": 1}]
		self.history = [{"Check": 1, "Call": 1, "Raise": 1, "Fold": 1},{"Check": 1, "Call": 1, "Raise": 1, "Fold": 1}]
	def setName(self, p1, p2):
		self.players[0].name = p2
		self.players[1].name = p1
	def genDeck(self):
		deck = []
		for num in range(13):
			for suit in range (4):
				deck.append(Card(num+2, suit))
		shuffle(deck) #this is actually not necessary
		return deck
	def drawCard(self):
		nextCard = random.choice(self.deck)
		self.deck.remove(nextCard)
		return nextCard
	def getCard(self):
		card = Card(1,2)
		while True:
			print "Input Suit:"
			suit = raw_input()
			if len(suit)==1:
				suit = card.getSuitOfChar(suit)
				break
			elif suit!="":
				print "Invalid"
		print "Input num:"
		while True:
			num = raw_input()
			if num!="":
				try:
					temp = int(num)
					break
				except ValueError:
					print "Invalid"
			else:
				temp = -1
		if temp!=-1:
			return Card(temp, suit)
		else:
			return None		
	def deal(self, debug=False, manual = False):
		if self.hasDelt:
			print "DEBUG: Deal called twice in a round"
			return
		if self.stage==0: #preflop
			for player in self.players:
				player.cards = [self.drawCard(), self.drawCard()]
			if manual:
				for i in range(len(self.players)-1):
					for j in range(2):
						print ("Input Card %d for Player %d (suit (SHDC) then number (2-14), enter empty for random:"%(j,i))
						temp = self.getCard()
						if temp!=None:
							self.players[i].cards[j] = temp
			if debug:
				print "Player zereo's hand: "
				print self.players[0].cards
				print "Player one's hand: "
				print self.players[1].cards
		elif self.stage==1: #flop
			self.table.append(self.drawCard())
			self.table.append(self.drawCard())
			self.table.append(self.drawCard())
			if manual:
				for i in range(3):
					print ("Input Card %d for flop (suit (SHDC) then number (2-14), enter empty for random:"%(i))
					temp = self.getCard()
					if temp!=None:
						self.table[i] = temp
			if debug:
				print "Flop: "
				print self.table
		elif self.stage==2: #turn
			self.table.append(self.drawCard())
			if manual:
				print "Input Turn"
				temp = self.getCard()
				if temp!=None:
					self.table[3]=temp
			if debug:
				print "Turn: "
				print self.table
		elif self.stage==3: #turn
			self.table.append(self.drawCard())
			if manual:
				print "Input Riveer"
				temp = self.getCard()
				if temp!=None:
					self.table[4]=temp
			if debug:
				print "River: "
				print self.table
		self.hasDelt = True
	#input: pocket cards for A, B, and table cards
	#outputs: tuple of scores (A wins if A>B)
	def checkWinnerM(self, pocketA, pocketB, table):
		maxA = 0;
		maxB = 0;
		cardA = [pocketA[0], pocketA[1]]+table #concat array
		cardB = [pocketB[0], pocketB[1]]+table
		for handA in itertools.combinations(cardA, 5):
			#print handA
			temp = Hand(handA).convert().ranking()
			if temp > maxA:
				maxA = temp
		for handB in itertools.combinations(cardB, 5):
			temp = Hand(handB).convert().ranking()
			if temp > maxB:
				maxB = temp
		return (maxA, maxB)
	#calls checkWinnerM for current game
	#returns a tuple of the hand values for a finished game
	def checkWinner(self):
		if self.stage!=4 and self.debug:
			print "Round not over or folded halfway"
			return
		res = self.checkWinnerM(self.players[0].cards, self.players[1].cards, self.table)
		self.runCallBacks(res[0]<res[1], "Won")
		return res
	#Either checks or calls depending on whether the oppenent raises (ie CallAll)
	def playerCheckCall(self, playerNum):
		if self.stage==4:
			print "DEBUG: Round already over, no more actions allowed", self.stage
			return
		if self.turn!=playerNum:
			print "DEBUG: Not this player's turn"
			return
		if self.actionRequired <= 1:
			if self.stage ==3:
				#print "Game finished"
				self.stage+=1
				#print self.checkWinner()
			else:
				self.betCurrentRound[playerNum]=self.betCurrentRound[not playerNum]
				self.turn = not self.turn
				self.runCallBacks(not self.turn, "Call")
				self.stats[playerNum]["Call"] += 1
				self._endStage_()
		else:
			self.actionRequired -= 1
			if self.stage==0:
				self.betCurrentRound[playerNum]=self.betCurrentRound[not playerNum]
				self.runCallBacks(not self.turn, "Call")
				self.stats[playerNum]["Call"] += 1
			else:
				self.runCallBacks(not self.turn, "Check")
				self.stats[playerNum]["Check"] += 1
				#print self.betCurrentRound[playerNum]
				#self.pot += self.raisesCurrentRound * self.highLimit
			self.turn = not self.turn
	#Check_fold: checks if allowed else fold
	def playerCheckFold(self, playerNum):
		if self.stage==4:
			print "DEBUG: Round already over, no more actions allowed"
			return
		if self.turn!=playerNum:
			print "DEBUG: Not this player's turn"
			return
		if self.actionRequired <= 1:
			if self.betCurrentRound[playerNum]<self.betCurrentRound[not playerNum]:
				self.playerFold(playerNum)
				if self.debug:
					print "Folding...",self.betCurrentRound[playerNum], self.betCurrentRound[not playerNum], self.dealer, playerNum
			else:
				if self.debug:
					print "Not folding...",self.betCurrentRound[playerNum], self.betCurrentRound[not playerNum], self.dealer, playerNum
				self.playerCheckCall(playerNum)
		else:
			if self.stage==0:
				self.playerFold(playerNum)
				return
			self.actionRequired -= 1
			self.turn = not self.turn
			self.runCallBacks(not self.turn, "Check")
			self.stats[playerNum]["Check"] += 1
	def playerRaise(self, playerNum):
		if self.stage==4:
			print "DEBUG: Round already over, no more actions allowed"
			return
		if self.turn!=playerNum:
			print "DEBUG: Not this player's turn"
			return
		if self.raisesCurrentRound==self.numRaisesAllowed:
			print "DEBUG: Max raises for this stage has been reached"
			return
		if self.stage>=2: #ie turn or river, use big bet
			self.betCurrentRound[playerNum]=self.betCurrentRound[not playerNum]+self.highLimit
		else:
			self.betCurrentRound[playerNum]=self.betCurrentRound[not playerNum]+self.lowLimit
		self.raisesCurrentRound+=1
		self.actionRequired-=1
		self.turn = not self.turn
		self.runCallBacks(not self.turn, "Raise")
		self.stats[playerNum]["Raise"]+=1
	def playerFold(self, playerNum):
		if self.stage==4:
			print "DEBUG: Round already over, no more actions allowed"
			return
		if self.turn!=playerNum:
			print "DEBUG: Not this player's turn"
			return
		self.players[not self.turn].cash += self.pot + self.betCurrentRound[self.turn]
		self.stage=4;
		self.actionRequired = -1;
		self.raisesCurrentRound = self.numRaisesAllowed;
		self.turn = not self.turn
		self.runCallBacks(not self.turn, "Fold")
		self.stats[playerNum]["Fold"]+=1
	def allowableActions(self,playerNum):
		# return (True,True,True,True)
		if self.turn!=playerNum or self.stage==4:
			return (False,False,False,False)
		checkAllowed = self.betCurrentRound[self.turn]==self.betCurrentRound[not self.turn]
		callAllowed = not checkAllowed
		foldAllowed = not checkAllowed #allow fold?
		raiseAllowed = (self.raisesCurrentRound<self.numRaisesAllowed)
		return (checkAllowed, callAllowed, raiseAllowed, foldAllowed)
	def performAction(self, action, playerNum):
		if self.debug:
			print "GAME: Player "+self.players[playerNum].name+" "+action+" on stage "+str(self.stage)
		if action=="Check":
			self.playerCheckCall(playerNum)
		elif action=="Call":
			self.playerCheckCall(playerNum)
		elif action=="Raise":
			self.playerRaise(playerNum)
		elif action=="CheckFold":
			self.playerCheckFold(playerNum)
		else:
			print "Bad action"
	def registerCallBack(self, fun, args):
		print "Registered"
		self.callBacks.append((fun, args))
	def deregisterCallBacks(self):
		self.callBacks = []
	
	def runCallBacks(self, player=1, action=""):
		for (fun, arg) in self.callBacks:
			fun(arg, (player, action))
	def performOneRound(self):
		#Deals player hands
		self.playerCheckCall(1)
		self.playerCheckCall(0)
		#Deals flop
		self.playerCheckCall(1)
		self.playerCheckCall(0)
		#Deals turn
		self.playerCheckCall(1)
		self.playerCheckCall(0)
		#Deals river
		self.playerCheckCall(1)
		self.playerCheckCall(0)
		#self.checkWinner()
		
	#you should now call these functions to progress the game state
	def endRound(self):
		res = self.checkWinner()
		if res!=None:
			self.players[res[0]<res[1]].cash+=self.pot
		self.hasDelt = False
		self.actionRequired = 2
		self.stage = 0
		#self.pot = self.lowLimit
		self.raisesCurrentRound = 0
		self.betCurrentRound = [0,0]
		self.betCurrentRound[self.dealer] = self.lowLimit
		self.betCurrentRound[not self.dealer] = self.lowLimit/2.0
		self.table = []
		self.deck = self.genDeck()
		self.deal(self.debug, self.manual)
		self.dealer = not self.dealer
		self.turn = self.dealer
		self.pot = 0
		for i in range(2):
			for stat in self.history[i]:
				self.history[i][stat] = self.history[i][stat]*0.9 + self.stats[i][stat]
		self.stats = [{"Check": 1, "Call": 1, "Raise": 1, "Fold": 1},{"Check": 1, "Call": 1, "Raise": 1, "Fold": 1}];
		#self.runCallBacks()
		return self.history
	def _endStage_(self):
		if self.debug:
			print "Stage End ", self.stage
		self.pot+=self.betCurrentRound[0]
		self.hasDelt = False
		self.actionRequired = 2
		self.raisesCurrentRound=0
		self.betCurrentRound = [0,0]
		self.stage+=1
		self.stage%=4;
		self.deal(self.debug, self.manual)
		self.turn = not self.dealer
		self.runCallBacks()

def adaptCards(cards):
	out = []
	for card in cards:
		out.append(card.getCardOfNum(card.num)+card.getCharOfSuit(card.suit))
	return out
def emulateRound(game):
	#Deals player hands
	game.deal()
	game.__endStage__()
	#Deals flop
	game.deal()
	game.__endStage__()
	#Deals turn
	game.deal()
	game.__endStage__()
	#Deals river
	game.deal()
	cardA = deepcopy(game.table)
	cardA.append(game.players[0].cards[0])
	cardA.append(game.players[0].cards[1])
	
	cardB = deepcopy(game.table)
	cardB.append(game.players[1].cards[0])
	cardB.append(game.players[1].cards[1])
	maxA = ()
	maxB = ()
	for handA in itertools.combinations(cardA, 5):
		#print handA
		temp = Hand(handA).convert().ranking()
		if temp > maxA:
		   maxA = temp
	for handB in itertools.combinations(cardB, 5):
		temp = Hand(handB).convert().ranking()
		if temp > maxB:
		   maxB = temp     
	print maxA>maxB
	print maxA
	print maxB
	game.__endRound__()

class Hand():
	def __init__(self, listOfCards):
		self.listOfCards = listOfCards
		self.ranks = []
		self.suits = []
		
	def convert(self):
		#self.listOfCards = ((5, 0), (9, 2), (14, 3), (12, 3), (8, 1))
		self.ranks = sorted([r.num for r in self.listOfCards])
		self.ranks.reverse()
		self.suits = [r.suit for r in self.listOfCards]
		return self

	def kind(self, n, biggest=1):
		count = 0
		prevRank = 0
		for r in self.ranks:
			if self.ranks.count(r) == n:
				if prevRank != r:
					count += 1
				if count == biggest:
					return (True, r)
			prevRank = r
		return (False,)

	def ranking(self):
		
		flush = len(set(self.suits)) == 1
		straight = (max(self.ranks)-min(self.ranks))==4 and len(set(self.ranks))==5


		if straight and flush:
			return 9, self.ranks
		if self.kind(4)[0]:
			
			return 8, self.kind(4)[1], self.kind(1)[1]
		if self.kind(3)[0] and self.kind(2)[0]:
			return 7, self.kind(3)[1], self.kind(2)[1]
		if flush:
			return 6, self.ranks
		if straight:
			return 5, self.ranks
		if self.kind(3)[0]:
			return 4, self.kind(3)[1], self.kind(1)[1], self.kind(1, 2)[1]
		if self.kind(2)[0] and self.kind(2, 2)[0]:
			return 3, self.kind(2)[1], self.kind(2, 2)[1], self.kind(1)[1]
		if self.kind(2)[0]:
			return 2, self.kind(2)[1], self.kind(1,1)[1], self.kind(1,2)[1], self.kind(1,3)[1]
		return 1, self.ranks
'''
for line in file("poker.txt"):
	print Hand(line[0:14]).convert().ranks, Hand(line[15:29]).convert().ranks
	print Hand(line[0:14]).convert().ranking(), Hand(line[15:29]).convert().ranking()
'''
