import pickle
import framework
from framework import Status
from framework import Auto_player
import UnbiasedNet
import numpy as np
import calling_station

net = UnbiasedNet.NeuralNet(framework.n_in,
                            framework.n_hidden, framework.n_out,
                            alpha=0.002, lamb=0.9, randomInit=True)
auto= Auto_player(net, "lion")
cs= calling_station.Calling_station()
for i in range(1000):
    auto.train(1, cs, frenzy=1)
    print i, auto.net.w_in[10][10], auto.net.w_out[10][0]
wins= []
for i in range(0):
    wins.append(auto.compete(cs, 4000, debug=0))
    print "win ", wins[i]
print np.mean(wins)
print np.std(wins)
pickle.dump(auto, open("lion.p","wb"))
