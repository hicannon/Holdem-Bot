import pickle
import framework
from framework import Status
from framework import Auto_player 
import UnbiasedNet
import numpy as np



auto=pickle.load(open("player.p", "rb"))
net2=UnbiasedNet.NeuralNet(framework.n_in ,framework.n_hidden, 
                           framework.n_out, False)
auto2=framework.Auto_player(net2)
wins= []
for i in range(1):
    wins.append(auto.compete(auto2,100))
print wins
print sum(wins)
#print auto.net.n_in, auto.net.n_hidden, auto.net.n_hidden, auto.net.w_out
#print auto2.net.w_out
print auto.net.w_in[1], auto2.net.w_in[1]
