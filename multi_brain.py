import framework.py as fw
import numpy as np
import holdem
import UnbiasedNet


class multi_brain(fw.Auto_player):
    def __init__(self, commander, num_of_bots, list_of_bots, 
                 stat=None, name= "anonymous", frenzy=False):
