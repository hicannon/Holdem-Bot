from HandStat import *
#from framework import *
import pickle
from UnbiasedNet import *
import call_defeater
import tight_aggressive
import framework
import numpy as np
import calling_station

csbot=calling_station.Calling_station()
preflop_net= UnbiasedNet.NeuralNet(framework.n_in, framework.n_hidden, 
                                   framework.n_out, alpha=0.001,lamb=0.9,
                                   randomInit=False, momentum=0,
                                   subdiv=[(0,0), (52, framework.n_hidden),
                                           (framework.n_in, 
                                            framework.n_hidden)])

preflop_bot= framework.Auto_player(preflop_net, name="preflop_bot")
bots= [preflop_bot]
for bot in bots:
    bot.train(100000, csbot, frenzy=True)
    pickle.dump(bot, open(bot.name+".p", "wb"))
for bot in bots:
    wins=[]
    for i in range(10):
        wins.append(bot.compete(csbot, 1000, debug=0))
    print "name= ", bot.name
    print wins
    print 'mean', np.mean(wins)
    print 'std', np.std(wins)
