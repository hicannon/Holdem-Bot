import pickle
list_of_opponents=[[1,    1,  0.001,  0.01],
                   [0.001,1,  0.1,    0.01],
                   [0.001,0.1, 1,     0.01],
                   [1,     1,   1,    0.1],
                   [5,     1,   1,    0.1],
                   [1,     5,   1,    0.1],
                   [1,     1,   5,    0.1],
                   [1,     1,   1,    1],
                   [5,     1,   1,    1],
                   [1,     5,   1,    1],
                   [1,     1,   5,    1]]

print list_of_opponents
pickle.dump(list_of_opponents, open("./bots/list_of_opponents.p", "wb"))
