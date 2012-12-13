import pickle
import UnbiasedNet
import anotherStatus as fw
from coarserStatus import AnotherStatus
from calling_station import Calling_station
from betting_station import Betting_station
from another_big_small_blind import Big_small_blind

result_name = 'result_lessFold_vs_betting.txt'
ALPHA = 0.005
n_train = 100000

stat_obj = AnotherStatus()
n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )

for LAMB in [0.7, 0.65]:
    
    name = 'coarser_lessFold_vs_betting_.005_' + str(LAMB) + '_1e5.p'
    
    print n_cards

    net1 = UnbiasedNet.NeuralNet(fw.n_in, n_cards, fw.n_out, randomInit=True,
                               alpha=ALPHA, lamb=LAMB)
    auto = fw.AnotherAutoPlayer(net1, name="auto1", check_prob=0.7,
                                call_prob=0.7, raise_prob=0.5, checkfold_prob=0.1)
    ai = Betting_station()
    auto.train(n_train, ai, debug=0, frenzy=1)
    pickle.dump(auto, open(name, "wb"))

    result = []
    for i in range(10):
        result.append( auto.compete(ai, 5000, debug=0) )
    data = '\n Learning rate: ' + str(ALPHA)
    data += '\n Lambda: ' + str(LAMB)
    data += '\n Number of training: ' + str(n_train)
    data += '\n Results: ' + str(result)
    print data
    
    
    with open(result_name, 'a') as f:
        f.write(data)
