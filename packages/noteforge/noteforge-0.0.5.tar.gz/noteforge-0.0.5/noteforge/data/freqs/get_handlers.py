from .mappings import *

def round_and_get_freq (freq : int) :
    return min(freqs,key=lambda x : abs(freq - x))

