import numpy as np

def setup_initial_c1c2(N, M):

    assert N % 2 == 0
    assert M % 2 == 0
    
    hw, hh = N//2, M//2

    c1_init = np.zeros((N, M))
    c1_init[:hw, :hh] = c1_init[hw:, hh:] = 3
    
    c2_init = np.zeros((N, M))
    c2_init[hw:, :hh] = c2_init[:hw, hh:] = 5

    return c1_init, c2_init