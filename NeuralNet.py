import numpy as np

def sigmoid(x, c=1):
    return 1.0 / (1 + np.exp( -c * x ))

def step(x):
    if x >= 0: return 1
    else: return 0

def biased(x):
    # add the entry 1 to the front of an list/array
    return np.append( 1, x )
    

class BiasedNeuralNet:

    def __init__(self, n_in, n_hidden, n_out,
                 alpha=0.5, lamb=1.0, randomInit=True):
        # Size of the network
        self.n_in = n_in
        self.n_hidden = n_hidden
        self.n_out = n_out
        # parameters
        self.alpha = alpha
        self.lamb = lamb
        # Weight vectors
        if randomInit:
            self.w_in = np.random.uniform(-.5, .5, (n_in + 1, n_hidden))
            self.w_out = np.random.uniform(-.5, .5, (n_hidden + 1, n_out))
        else:
            self.w_in = (np.eye(n_in + 1, n_hidden) -
                         np.eye(n_in + 1, n_hidden, k=-1))
            self.w_out = np.ones((n_hidden + 1, n_out))

    ###### Predicting
    def in_to_hidden(self, x):
        # Given x, an array of n_in input,
        # return a np.array of the hidden
        return sigmoid(np.dot( biased(x), self.w_in ))

    def hidden_to_out(self, h):
        # Given h, an array of n_out hidden input,
        # return the predicted real valued
        return np.dot( biased( h ), self.w_out )

    def predict(self, x):
        # Given input, return a 1d np.array of real-valued output
        return self.hidden_to_out( self.in_to_hidden( x ) )

    ############# supervised Learning
    def learnOnline(self, x, y, alpha=.5, beta=.5):
        '''
        learning for neural network
        '''
        # hBiased is 2-dimensional: 1 by n_hidden+1
        hBiased = biased(self.in_to_hidden(x))[np.newaxis, :]
        h = hBiased[:,1:]
        xBiased = biased(x)[np.newaxis, :]
        o = self.predict(x)
        error_out = y - o
        delta_out = error_out
        delta_in =  h * (1 - h) * np.dot( error_out,
                                          np.transpose(self.w_out[1:,:]) )
        # n_hidden+1 by 1 * n_out gives n_hidden+1 by n_out
        self.w_out += beta * np.transpose(hBiased) * delta_out
        # n_in+1 by 1 * n_hidden gives n_in+1 by n_hidden
        self.w_in += alpha * np.transpose(xBiased) * delta_in

    def learnTD(self, xLis, y):
        '''
        matrix implementation of learnTD
        learning for 1 entire round, with x being a 2d array
        and y be the payout at the end
        '''
        ## tdLearn and learnTD should be the same thing after they are tested
        trace_in = np.zeros((self.n_in+1, self.n_hidden, self.n_out))
        trace_out = np.zeros((self.n_hidden+1, self.n_out))
        w_out_change = np.zeros((self.n_hidden+1, self.n_out))
        w_in_change = np.zeros((self.n_in+1, self.n_hidden))
        for i in range(len(xLis)):
            # n_in + 1
            currX = xLis[i]
            xBiased = biased( currX )
            # n_hidden + 1 by 1
            hBiased = biased( self.in_to_hidden( currX ) )[:, np.newaxis]
            # n_out
            currY = self.predict( currX )
            if i < len(xLis) - 1:
                nextY = self.predict( xLis[i+1] )
                error_out = nextY - currY
            else: # last update's reward is the payout y.
                error_out = y - currY
            trace_out *= self.lamb
            trace_in *= self.lamb
            trace_out += hBiased
            # n_hidden by 1
            h = hBiased[1:, :]
            grad_in = ( (self.w_out[1:,:] * h * (1-h))[np.newaxis, :, :] *
                        xBiased[:, np.newaxis, np.newaxis] )
            trace_in += grad_in
            w_out_change += self.alpha * error_out * trace_out         
            w_in_change += self.alpha * np.dot( error_out,
                                           np.transpose(trace_in, [0,2,1]) )
            
        self.w_out += w_out_change
        self.w_in += w_in_change

'''
from random import randint
class Walk:
    def __init__(self, width=10, start=5, randomInit=True):
        # 0, ..., width-1 are the positions
        # 1, ..., width-2 are the unfinished position
        self.width = width
        self.startPos = start
        self.position = start
        self.neural = NeuralNet( self.width, 2, 1, randomInit=randomInit )
        self.actionLis = []
        self.rewardDic = {}

    def _move(self, amount):
        # change self.position by the amount input
        self.position += amount
    def _moveLeft(self):
        self.position += -1
    def _moveRight(self):
        self.position += 1

    def binaryPosition(self, shift=0, position=None):
        # returns the binary representation of current position
        if position is None:
            position = self.position
        lis = [0] * self.width
        lis[ position + shift ] = 1
        return lis

    def bestAction(self, position=None):
        if position is None:
            position = self.position
        leftsReward = self.neural.predict(self.binaryPosition( -1, position))
        rightsReward = self.neural.predict(self.binaryPosition( 1, position ))
        if rightsReward > leftsReward:
            return 1
        else:
            return -1

    def _actRandom(self):
        # move -1 or +1 with probability 0.5
        self._move( randint(0,1)*2 - 1 )

    def _actDirect(self):
        if self.startPos < self.position:
            self._move(1)
        elif self.startPos > self.position:
            self._move(-1)
        else:
            self._move( randint(0,1)*2 - 1 )

    def supervisedLearning(self, left=True):
        if left:
            self.neural.learnOnline( [1, 0, 0], 5 )
        else:
            self.neural.learnOnline( [0, 0, 1], -5 )
        
    def playAndLearn(self, how=0, matrix=True):
        # Use the random walk strategy to play
        # Updates the weights using tdLearn
        # Reward 10 points for reaching position 0
        # Punish 10 points for reaching the right
        # Punish 1 point for each nonfinishing step
        xLis = []
        y = 0
        while( 0 < self.position and self.position < self.width - 1):
            xLis.append( self.binaryPosition() )
            y -= 1
            if how==0:
                how = self._actDirect
            how() # one can put in self._actDirect() as well
        xLis.append( self.binaryPosition() )
        # Reward and restart
        if self.position == 0:
            y += 5
        else:
            y -= 5
        self.restart()
        # learn
        if matrix==True:
            self.neural.tdLearn(xLis, y)
        else:
            self.neural.learnTD(xLis, y)

    def isChanged(self):
        # return 1 if any action is changed
        lis = [self.bestAction(position=i) for i in range(1, self.width-1)]
        if lis != self.actionLis:
            self.actionLis = lis
            return 1
        else: return 0
            
    def playGreedy(self):
        # use self._actGreedy and display the results
        print("Currently at ", self.position)
        while( 0 < self.position and self.position < self.width - 1):
            self._move( self.bestAction() )
            print("Currently at ", self.position)

    def predictReward(self):
        for i in range(1, self.width-1):
            leftsReward = self.neural.predict(self.binaryPosition(-1, i))
            rightsReward = self.neural.predict(self.binaryPosition(1, i))
            self.rewardDic[i] = (leftsReward[0], rightsReward[0])
        return self.rewardDic

    def restart(self):
        # start a new game
        self.position = self.startPos
        
game = Walk(width=3, start=1, randomInit=False)
another = Walk(width=3, start=1, randomInit=False)
print game.predictReward()
print another.predictReward()
for i in range(10):
    game.playAndLearn(how=game._moveLeft, matrix=True)
    another.playAndLearn(how=another._moveLeft, matrix=False)
    print another.predictReward()
    print game.predictReward()
'''
