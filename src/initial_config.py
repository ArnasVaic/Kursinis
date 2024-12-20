import numpy as np

def get_c_init(N, M, c0):

  assert N % 2 == 0
  assert M % 2 == 0

  hw, hh = N//2, M//2

  c1_init = np.zeros((N, M))
  c1_init[:hw, :hh] = c1_init[hw:, hh:] = 3 * c0

  c2_init = np.zeros((N, M))
  c2_init[hw:, :hh] = c2_init[:hw, hh:] = 5 * c0

  return c1_init, c2_init, np.zeros((N, M))
