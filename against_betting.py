import pickle
import UnbiasedNet
import anotherStatus as fw
#from coarserStatus import AnotherStatus
from calling_station import Calling_station
from betting_station import Betting_station
from another_big_small_blind import Big_small_blind
import specified_prob


good_vs_betting=pickle.load(open("./bots/goodbot_less_fold_coarser_true_vs_betting_.005_0.65.p", "rb"))

ai=Betting_station()
result = []
for i in range(10):
    result.append( good_vs_betting.compete(ai, 5000, debug=0) )
print '\n Results: ', result

    
