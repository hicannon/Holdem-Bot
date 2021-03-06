import pickle
import UnbiasedNet
import anotherStatus as fw
#from coarserStatus import AnotherStatus
from calling_station import Calling_station
from betting_station import Betting_station
from another_big_small_blind import Big_small_blind
import specified_prob

result_name = 'result_coarser_blind_vs_betting.txt'
ALPHA = 0.005
n_train = 100000
list_of_bots= pickle.load(open("list_of_opponents.p", "rb"))

stat_obj = fw.AnotherStatus()
n_cards = sum( len(stat_obj.vec_cards[key]) for key in stat_obj.vec_cards )
check_prob=0.5
call_prob=0.5
raise_prob=0.001
checkfold_prob=0.15

for LAMB in [0.6, 0.65,0.7]:
    name = ('specified_training_vs_calling_.005_' + 
            str(LAMB)+'_' +str(check_prob)
            +'_'+ str(call_prob) +'_'+ str(raise_prob) 
            +'_'+str(checkfold_prob) +'.p')
    print n_cards
    net1 = UnbiasedNet.NeuralNet(fw.n_in, n_cards, fw.n_out, randomInit=True,
                               alpha=ALPHA, lamb=LAMB,
                                subdiv=[(0,0), (n_cards,n_cards),
                                        (fw.n_in,n_cards)])
    auto = fw.AnotherAutoPlayer(net1, name="auto1", check_prob=check_prob,
                                call_prob=call_prob, raise_prob=raise_prob, 
                                checkfold_prob=checkfold_prob)
    ai = specified_prob.Specified_prob(prob_list={
            'Check':list_of_bots[0][0], 'Call':list_of_bots[0][1], 
            'Raise':list_of_bots[0][2], 
            'CheckFold':list_of_bots[0][3]})
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
