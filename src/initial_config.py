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

def get_larger_c_init(N, M, c0):
  assert N % 4 == 0
  assert M % 4 == 0

  # pattern of this initial configuration
  # ('-' for c1, 'O' for c2)
  # O - - O
  # - O O -
  # - O O -
  # O - - O

  c1_init, c2_init = np.zeros((N, M)), np.zeros((N, M))

  qw, qh = N // 4, M // 4

  # c1
  c1_init[qw:N - qw, :qh] = 3 * c0
  c1_init[qw:N - qw, N - qh:] = 3 * c0

  c1_init[:qw, qh:M - qh] = 3 * c0
  c1_init[N - qw:, qh:M - qh] = 3 * c0

  # c2
  c2_init[:qw, :qh] = 5 * c0
  c2_init[N - qw:, :qh] = 5 * c0
  c2_init[:qw, M - qh:] = 5 * c0
  c2_init[N - qw:, M - qh:] = 5 * c0

  c2_init[qw:N - qw, qh:M - qh] = 5 * c0

  return c1_init, c2_init, np.zeros((N, M))