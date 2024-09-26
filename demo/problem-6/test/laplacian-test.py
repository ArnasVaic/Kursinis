# %%
# suboptimal implementation yields solutions
# where each elements gets consumed at *constant*
# rate (at least it seems so from the quantity graphs)
# but in reality it should slow down as the time passes
# like in the optimized solution. This is a test to
# see if my laplacian operator implementation differs
# from the optimized version

import numpy as np
from scipy.signal import convolve2d

DX, DY = 1, 1

# suboptimal implementation of laplacian
def suboptimal_lap(c, x, y, s): 
  c_left = c[x, y] if x == 0 else c[x - 1, y]
  c_right = c[x, y] if x == s - 1 else c[x + 1, y]
  c_top = c[x, y] if y == 0 else c[x, y - 1]
  c_bottom = c[x, y] if y == s - 1 else c[x, y + 1]
  lap_x = (c_left - 2 * c[x, y] + c_right) / (DX**2)
  lap_y = (c_top - 2 * c[x, y] + c_bottom) / (DY**2)
  return lap_x + lap_y

    # optimal laplacian implementation
ONE_OVER_DX2 = 1 / DX**2
ONE_OVER_DY2 = 1 / DY**2
DIFF_KERNEL = np.array([
  [0, ONE_OVER_DY2, 0],
  [ONE_OVER_DX2, -2 * ( ONE_OVER_DX2 + ONE_OVER_DY2 ), ONE_OVER_DX2],
  [0, ONE_OVER_DY2, 0]
])

def optimal_lap(c):
  padded = np.pad(c, (1, 1), 'edge')
  return convolve2d(padded, DIFF_KERNEL, mode='valid')


print(f'eps: {np.finfo(float).eps}')

for s in range(4, 100):
  c = np.random.rand(s, s)

  suboptimal_result = np.zeros((s, s))
  for x in range(s):
    for y in range(s):
      suboptimal_result[x, y] = suboptimal_lap(c, x, y, s)

  optimal_result = optimal_lap(c)
  sq_diff = np.square(suboptimal_result - optimal_result)
  error = np.sum(sq_diff)
 
  assert error < np.finfo(float).eps

# %%
