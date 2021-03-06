import pickle
#import UnbiasedNet
from biasedPerceptron import BiasedPerceptron
import coarserStatus as fw
from calling_station import Calling_station
from betting_station import Betting_station 
from specified_prob import Specified_prob

ALPHA = 0.005
n_train = 100000

stat_obj = fw.AnotherStatus()
n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )

for ALPHA in [0.01,0.001,0.0005]:
    name = 'biasedPerceptron_vs_raising_.005_' + str(ALPHA) + '_1e6.p'
    print n_cards
    net = BiasedPerceptron(fw.n_in, n_cards, fw.n_out, randomInit=True,
                               alpha=ALPHA, lamb=0.7)
    auto = fw.AnotherAutoPlayer(net, name="superbot")
    ai = Specified_prob(prob_list={'Check':0.01, 'Call':0.1, 'Raise':0.99, 
                        'CheckFold':0.01})
    auto.train(n_train, ai, debug=0, frenzy=1)
    pickle.dump(auto, open(name, "wb"))
    result = []
    for i in range(10):
        result.append( auto.compete(ai, 5000, debug=0) )
    data = '\n Learning rate: ' + str(ALPHA)
    data += '\n Lambda: ' + str(LAMB)
    data += '\n Number of training: ' + str(n_train)
    data += '\n Results: ' + str(result)
    
    result_name = 'result_' + name[:-2] +  '.txt'
    with open(result_name, 'w') as f:
        f.write(data)
    print data
