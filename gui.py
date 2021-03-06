import Tkinter
from tkFileDialog import askopenfilename
from tkSimpleDialog import askinteger
import pickle
from human_player import Human_player
from Tkinter import *
from holdem import *
#from PIL import Image, ImageTk
from framework import *
from threading import Thread
import time
from multi_brain import Multi_brain
#from HandStat import *

running = False
class SimulationThread(Thread):
	def __init__(self, p1, p2, game):
		Thread.__init__(self)
		self.p1 = p1
		self.p2 = p2
		self.game = game
	def run(self):
		global running
		self.p1.status=Status()
		self.p2.status=Status()
		#TODO get winnings
		self.p1.sim_one_hand(self.p2, self.game, dealer=not self.game.dealer, debug=1)
		running = False
	def kill(self):
		pass
		#raise NameError("Killed")
class HoldemGUI():
	def __init__(self):
		self.game = None
		self.p1 = None
		self.p2 = Human_player()
		self.manual = False
		tk = Tkinter
		
		root = tk.Tk()
		#cv = tk.Canvas(root, width=800, height=600)
		#cv.pack(side=tk.LEFT)
		
		#load card images
		c = Card(1,1)
		self.cards= {}
		for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
			for card in range(2,15):
				#self.cards[card, suit[0]]=tk.PhotoImage(Image.open("D:/Dropbox/CS4780/Project/Machine-Learning/cards/"+suit+"/"+c.getCardOfNum(card)+suit[0]+".eps"))
				self.cards[card, suit[0]] = tk.PhotoImage(file="./cards_gif/"+suit[0].lower()+c.getCardOfNum(card).lower()+".gif")
		self.unknownCard = tk.PhotoImage(file="./cards_gif/b2fv.gif")
		root.title("Hold'em Poker")
		root.minsize(800, 600)

		#need self.backbround b/c python garbage collects it otherwise
		self.backGround = tk.PhotoImage(file="./bkg.gif")
		backGroundLabel = tk.Label(root, image=self.backGround)
		backGroundLabel.place(x=0,y=0, relwidth=1, relheight=1)
		
		tpFrame = tk.Frame(root)
		tpFrame.pack(side = tk.TOP, fill = tk.Y)
		
	
		self.newGameB = tk.Button(tpFrame, text="New Game", command=self.newGame)
		self.newGameB.config(state=DISABLED)
		self.newGameB.pack(side=tk.LEFT)
		
		loadBotB = tk.Button(tpFrame, text="Load Bot", command=self.loadBot)
		loadBotB.pack(side=tk.LEFT)
		
		showCardsB = tk.Button(tpFrame, text="Show Hand", command = self.displayPocketCards)
		showCardsB.pack(side=tk.LEFT)
		
		resetB = tk.Button(tpFrame, text="Reset Buttons", command = self.toggleButtons)
		resetB.pack(side=tk.LEFT)
		
		manualB = tk.Button(tpFrame, text="Manual Toggle", command = self.toggleManual)
		manualB.pack(side=tk.LEFT)
		
		p1ActionFrame = tk.Frame(root)
		p1ActionFrame.pack(side=tk.TOP, fill = tk.Y)
		self.p1Action = tk.StringVar()
		p1ALabel = tk.Label(p1ActionFrame, textvariable=self.p1Action)
		p1ALabel.pack(side=tk.LEFT)
		
		self.p1Money = tk.StringVar()
		p1MLabel = tk.Label(p1ActionFrame, textvariable=self.p1Money, bg="yellow")
		p1MLabel.pack(side=tk.LEFT)
		
		self.p1Dealer = tk.StringVar()
		p1DLabel = tk.Label(p1ActionFrame, textvariable=self.p1Dealer)
		p1DLabel.pack(side=tk.RIGHT)
		
		#holds the frames for displaying each player's cards as well as table
		tableFrame = tk.Frame(root, width=800, height=600)
		tableFrame.place(in_=root, anchor="c", relx=.5, rely=.5)
		
		#tableStatusFrame = tk.Frame(tableFrame, bg="green")
		self.statusMessage = tk.StringVar()
		tableStatusLabel = tk.Label(tableFrame, bg="green",textvariable=self.statusMessage)
		tableStatusLabel.pack(side=tk.TOP, fill=tk.Y);
		
		p1Cust = tk.Frame(tableFrame, width=800, height=100)
		self.p1Cust1 = StringVar()
		p1CustEntry1 = Entry(p1Cust,textvariable = self.p1Cust1)
		p1CustEntry1.pack(side=tk.LEFT, fill=tk.X)
		self.p1Cust2 = StringVar()
		p1CustEntry2 = Entry(p1Cust,textvariable = self.p1Cust2)
		p1CustEntry2.pack(side=tk.LEFT, fill=tk.X)
		#p1Cust.pack(side=tk.TOP)
		
		#tableFrame.pack(side=tk.TOP, fill=tk.Y)
		p1Frame = tk.Frame(tableFrame, bg="white", width=800, height=100)
		p1Frame.pack(side=tk.TOP)
		
		self.p1Card1 = Label(p1Frame, text = "P1 C1")
		self.p1Card1.pack(side=tk.LEFT, fill=tk.X)
		self.p1Card2 = Label(p1Frame, text = "P1 C2")
		self.p1Card2.pack(side=tk.LEFT, fill=tk.X)
		
		communityCust = tk.Frame(tableFrame, width=800, height = 400)
		self.fCust1 = StringVar()
		self.fCust2 = StringVar()
		self.fCust3 = StringVar()
		self.tCust = StringVar()
		self.rCust = StringVar()
		fCust1Entry = Entry(communityCust,textvariable = self.fCust1)
		fCust1Entry.pack(side=tk.LEFT, fill=tk.X)
		fCust2Entry = Entry(communityCust,textvariable = self.fCust2)
		fCust2Entry.pack(side=tk.LEFT, fill=tk.X)
		fCust3Entry = Entry(communityCust,textvariable = self.fCust3)
		fCust3Entry.pack(side=tk.LEFT, fill=tk.X)
		tCustEntry = Entry(communityCust,textvariable = self.tCust)
		tCustEntry.pack(side=tk.LEFT, fill=tk.X)
		rCustEntry = Entry(communityCust,textvariable = self.rCust)
		rCustEntry.pack(side=tk.LEFT, fill=tk.X)
		#communityCust.pack(side=tk.TOP, fill=tk.BOTH)
		
		communityFrame = tk.Frame(tableFrame, width=800, height=400)
		#labels hold will hold cards
		self.f1Card = Label(communityFrame, text = "Flop1")
		self.f1Card.pack(side=tk.LEFT)
		self.f2Card = Label(communityFrame, text = "Flop2")
		self.f2Card.pack(side=tk.LEFT)
		self.f3Card = Label(communityFrame, text = "Flop3")
		self.f3Card.pack(side=tk.LEFT)
		self.tCard = Label(communityFrame, text = "Turn")
		self.tCard.pack(side=tk.LEFT)
		self.rCard = Label(communityFrame, text = "River")
		self.rCard.pack(side=tk.LEFT)
		communityFrame.pack(side=tk.TOP)
		
		p2Frame = tk.Frame(tableFrame, width=800, height=100)
		p2Frame.pack(side=tk.BOTTOM)
		p2Cust = tk.Frame(tableFrame, width=800, height=100)
		self.p2Cust1 = StringVar()
		p2CustEntry1 = Entry(p2Cust,textvariable = self.p2Cust1)
		p2CustEntry1.pack(side=tk.LEFT, fill=tk.X)
		self.p2Cust2 = StringVar()
		p2CustEntry2 = Entry(p2Cust,textvariable = self.p2Cust2)
		p2CustEntry2.pack(side=tk.LEFT, fill=tk.X)
		#p2Cust.pack(side=tk.TOP)
		
		self.p2Card1 = tk.Label(p2Frame, text = "P2 C1", image = None)
		self.p2Card1.pack(side=tk.LEFT)
		self.p2Card2 = Label(p2Frame, text = "P2 C2")
		self.p2Card2.pack(side=tk.LEFT)
		
		#Frame holding player action button
		btFrame = tk.Frame(root)
		btFrame.pack(side=tk.BOTTOM, fill = tk.Y)
		
		p2ActionFrame = tk.Frame(root)
		p2ActionFrame.pack(side=tk.BOTTOM, fill = tk.Y)
		
		self.p2Action = tk.StringVar()
		p2ALabel = tk.Label(p2ActionFrame, textvariable=self.p2Action)
		p2ALabel.pack(side=tk.LEFT)
		
		self.p2Money = tk.StringVar()
		p2MLabel = tk.Label(p2ActionFrame, textvariable=self.p2Money, bg="yellow")
		p2MLabel.pack(side=tk.LEFT)
		
		self.p2Dealer = tk.StringVar()
		p2DLabel = tk.Label(p2ActionFrame, textvariable=self.p2Dealer)
		p2DLabel.pack(side=tk.RIGHT)
		
		self.checkB = tk.Button(btFrame, text="Check", command=self.pCheck)
		self.checkB.pack(side=LEFT)
		self.callB = tk.Button(btFrame, text = "Call", command=self.pCall)
		self.callB.pack(side=LEFT)
		self.raiseB = tk.Button(btFrame, text="Raise", command=self.pRaise)
		self.raiseB.pack(side=LEFT)
		self.foldB = tk.Button(btFrame, text="Fold", command=self.pFold)
		self.foldB.pack(side=LEFT)
		self.endRoundB = tk.Button(btFrame, text="End Round", command=self.pEndRound)
		self.endRoundB.pack(side=LEFT)
	def pCheck(self):
		if self.game.actionRequired==2:
			print "Actually a checkFirst"
			self.p2.humanAction("Check")
		else:
			self.p2.humanAction("CheckFold")
		#self.p2Action.set("Check")
		self.toggleButtons()
	def pRaise(self):
		#self.p2Action.set("Raise")
		self.p2.humanAction("Raise")
		self.toggleButtons()
	def pCall(self):
		#self.p2Action.set("Call")
		self.p2.humanAction("Call")
		self.toggleButtons()
	def pFold(self):
		#self.p2Action.set("Fold")
		self.p2.humanAction("CheckFold")
		self.toggleButtons()
	def updateAction(self, args):
		(player, action) = args
		if player==0:
			self.p1Action.set(action)
			self.p2Action.set("")
		elif player==1:
			self.p2Action.set(action)
			self.p1Action.set("")
		if action=="Fold":
			if player==0:
				self.p2Action.set("Won by default")
			elif player==1:
				self.p1Action.set("Won by default")
	def toggleButtons(self, ignored=None):
		time.sleep(0)
		(checkAllowed, callAllowed, raiseAllowed, foldAllowed) = self.game.allowableActions(1)
		if checkAllowed:
			self.checkB.config(state=NORMAL)
		else:
			self.checkB.config(state=DISABLED)
		if callAllowed:
			self.callB.config(state=NORMAL)
		else:
			self.callB.config(state=DISABLED)
		if raiseAllowed:
			self.raiseB.config(state=NORMAL)
		else:
			self.raiseB.config(state=DISABLED)
		if foldAllowed:
			self.foldB.config(state=NORMAL)
		else:
			self.foldB.config(state=DISABLED)
		self.updateTableCards()
	def pEndRound(self):
		self.game.endRound()
		self.playHand()
		self.cleanUpCards()
		self.displayPocketCards(2)
	def newGame(self):
		if self.game!=None:
			self.game.deregisterCallBacks()
		lowBlind = askinteger("Table Options", "Small Blind", initialvalue="5")
		if lowBlind==None:
			lowBlind=5
		highBlind = askinteger("Table Options", "Large Blind", initialvalue="10")
		if highBlind==None:
			highBlind=10
		self.game = Holdem(lowBlind,highBlind, debug=True, manual = self.manual)
		print self.game.stage
		self.game.registerCallBack(HoldemGUI.toggleButtons, self)
		self.game.registerCallBack(HoldemGUI.updateAction, self)
		self.cleanUpCards()
		self.displayPocketCards(2)
		self.toggleButtons()
		self.playHand()
	#Note this might be problematic if sim_one_hand hangs for some reason
	def playHand(self):
		global running
		if running:
			print "Simulation thread still running, further actions will lead to kittens dying\n"
			print "Attempting to kill..."
			print "Begin IGNORE================"
			self.game.deregisterCallBacks()
			
			try:
				while self.simThread.is_alive():
					self.p2.humanAction("Fold")
					self.simThread.join(1)
				#self.simThread.kill()
			except NameError:
				print "Killed?"
			print "End IGNORE=================="
			self.game.registerCallBack(HoldemGUI.toggleButtons, self)
			self.game.registerCallBack(HoldemGUI.updateAction, self)
		if running:
			print "Failed to kill"
		running=True
		self.simThread = SimulationThread(self.p1,self.p2,self.game)
		self.simThread.start()
		self.toggleButtons()
	def toggleManual(self):
		self.manual = not self.manual
		print "Manual mode is ",self.manual
		self.game.manual = self.manual
		#if len(self.game.table)>=3:
		#	self.game.table[0].self.f1Cust1.get()
	def updateTableCards(self):
		if len(self.game.table)>=3:
			self.f1Card.config(image = self.cards[self.game.table[0].num, self.game.table[0].getCharOfSuit(self.game.table[0].suit)])
			self.f2Card.config(image = self.cards[self.game.table[1].num, self.game.table[1].getCharOfSuit(self.game.table[1].suit)])
			self.f3Card.config(image = self.cards[self.game.table[2].num, self.game.table[2].getCharOfSuit(self.game.table[2].suit)])
			#self.fCust1.set(self.game.table[0].getCharOfSuit(self.game.table[0].suit)+str(self.game.table[0].num))
			#self.fCust2.set(self.game.table[1].getCharOfSuit(self.game.table[1].suit)+str(self.game.table[1].num))
			#self.fCust3.set(self.game.table[2].getCharOfSuit(self.game.table[2].suit)+str(self.game.table[2].num))
		if len(self.game.table)>=4:
			self.tCard.config(image = self.cards[self.game.table[3].num, self.game.table[3].getCharOfSuit(self.game.table[3].suit)])
			#self.tCust.set(self.game.table[3].getCharOfSuit(self.game.table[3].suit)+str(self.game.table[3].num))
		if len(self.game.table)>=5:
			self.rCard.config(image = self.cards[self.game.table[4].num, self.game.table[4].getCharOfSuit(self.game.table[4].suit)])
			#self.rCust.set(self.game.table[4].getCharOfSuit(self.game.table[4].suit)+str(self.game.table[4].num))
		self.statusMessage.set("Pot: "+str(self.game.pot))
	#0 to display 0, 1 to display player 1, 2 to display all
	def displayPocketCards(self, player=2):
		#print "Called"
		if self.game==None:
			return
		if player==1 or player==2:
			p2Cards = self.game.players[1].cards
			self.p2Card1.config(image = self.cards[p2Cards[0].num, p2Cards[0].getCharOfSuit(p2Cards[0].suit)])
			self.p2Card2.config(image = self.cards[p2Cards[1].num, p2Cards[1].getCharOfSuit(p2Cards[1].suit)])
			self.p2Cust1.set(p2Cards[0].getCharOfSuit(p2Cards[0].suit)+str(p2Cards[0].num))
			self.p2Cust2.set(p2Cards[1].getCharOfSuit(p2Cards[1].suit)+str(p2Cards[1].num))
		if player==0 or player==2:
			p1Cards = self.game.players[0].cards
			self.p1Card1.config(image = self.cards[p1Cards[0].num, p1Cards[0].getCharOfSuit(p1Cards[0].suit)])
			self.p1Card2.config(image = self.cards[p1Cards[1].num, p1Cards[1].getCharOfSuit(p1Cards[1].suit)])
			self.p1Cust1.set(p1Cards[0].getCharOfSuit(p1Cards[0].suit)+str(p1Cards[0].num))
			self.p1Cust2.set(p1Cards[1].getCharOfSuit(p1Cards[1].suit)+str(p1Cards[1].num))
		self.p1Money.set("   Winnings: "+str(self.game.players[0].cash))
		self.p2Money.set("   Winnings: "+str(self.game.players[1].cash))
		if self.game.dealer:
			self.p1Dealer.set("")
			self.p2Dealer.set("D")
		else:
			self.p2Dealer.set("")
			self.p1Dealer.set("D")
			
		#self.p2Card1.config(image = self.backGround)
	def cleanUpCards(self):
		self.f1Card.configure(image=self.unknownCard)
		self.f2Card.config(image=self.unknownCard)
		self.f3Card.config(image=self.unknownCard)
		self.tCard.config(image=self.unknownCard)
		self.rCard.config(image=self.unknownCard)
		self.p1Card1.config(image=self.unknownCard)
		self.p2Card2.config(image=self.unknownCard)
		self.p1Card2.config(image=self.unknownCard)
		self.p2Card1.config(image=self.unknownCard)
		self.p1Action.set("")
		self.p2Action.set("")
	def loadBot(self):
		filename = askopenfilename()
		if filename=="":
			return
		self.p1 = pickle.load(open(filename, "rb"))
		self.p1.debug=True
		self.newGameB.config(state=NORMAL)
		self.newGame()
	#t.ondrag(clickHandler)
	def startGUI(self):
		Tkinter.mainloop()

if __name__=="__main__":
	HoldemGUI().startGUI()
