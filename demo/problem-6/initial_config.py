import numpy as np

def setup_initial_c1c2(N, M):

    assert N % 2 == 0
    assert M % 2 == 0

    c1_init, c2_init = np.zeros((N, M)), np.zeros((N, M))
    hw, hh = int(N/2), int(M/2)

    amount = 200 / ( N * M )

    c1_init[:hw, :hh] = c1_init[hw:, hh:] = 3 * amount
    c2_init[hw:, :hh] = c2_init[:hw, hh:] = 5 * amount

    return c1_init, c2_init