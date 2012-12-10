import numpy as np
import holdem
import UnbiasedNet
import framework as fw

class Betting_station(fw.Auto_player):
    def __init__(self):
        self.net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                                        randomInit=False)
        self.status= fw.Status()
        self.name="BettingStation"
    def decision(self, player2, gameO=None, playerNum=-1, debug=0):
        #always call/check
        if debug:
            print "it's the bs's turn!"
        stage=self.status.stage
        if (self.status.vec_act[stage][0]< self.status.vec_act[stage][1]):
            if debug:
                print "Now bs call at stage ", stage
            next=self.status.call()
            action= "Call"
        else:
            next=self.status.praise()
            if debug:
                print "Now bs bet/raise at stage ", stage
            action= "Raise"
        self.status= next.copy()
        #update the other guy's status vector resulting from your act
        player2.status.vec_act[stage][1]=self.status.vec_act[stage][0]
        player2.status.vec_act[stage][2]=self.status.vec_act[stage][2]
        player2.status.stage= self.status.stage
        return action

if __name__== "__main__":
    import pickle
#    auto= pickle.load(open("player.p", "rb"))
    net= UnbiasedNet.NeuralNet(fw.n_in, fw.n_hidden, fw.n_out,
                               alpha=0.02, 
                               lamb=0.9, randomInit=True)
    auto= fw.Auto_player(net, name="superbot") 
    bs= Betting_station()
    auto.train(10,bs, debug=1)
    pickle.dump(auto, open("player.p", "wb"))
    
    
