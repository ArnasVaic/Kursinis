# %%

import numpy as np
import numpy.typing as npt
import configparser
from tqdm import tqdm
from simid import simulation_identifier

config = configparser.ConfigParser() 
config.read('simulation-parameters.ini')
params = config['DEFAULT']

L = float(params['L'])
T = int(params['T'])
DX = float(params['DX'])
DY = float(params['DY'])
D = float(params['D'])
K1 = float(params['K1'])
K2 = float(params['K2'])
K3 = float(params['K3'])

# Discretized plate size
SIZE_X, SIZE_Y = int(L / DX), int(L / DY)

# c_i(x, y, t), (x, y, t) ∈ [0, L] x [0, L] x [0, T]
c1 = np.zeros([SIZE_X, SIZE_Y, T])
c2 = np.zeros([SIZE_X, SIZE_Y, T])
c3 = np.zeros([SIZE_X, SIZE_Y, T])

# Initial conditions at t = 0:
# 4 non-overlapping blocks of different materials (c1 and c2)
c1[:int(SIZE_X/2), :int(SIZE_Y/2), 0] = 1
c1[int(SIZE_X/2):, int(SIZE_Y/2):, 0] = 1

c2[int(SIZE_X/2):, :int(SIZE_Y/2), 0] = 1
c2[:int(SIZE_X/2), int(SIZE_Y/2):, 0] = 1

# DT size depends on the maximum c1/c2 value
DT1 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 3 * np.max(c2[:, :, 0]))
DT2 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 5 * np.max(c1[:, :, 0]))
DT = np.min([DT1, DT2])

def laplacian(f: npt.NDArray[np.float64], x0: int, y0: int) -> np.float64:
  """Calculate the Laplacian of function f at point (x0, y0). Additionally, assume boundary conditions to be df/dn=0 where n is the normal vector along the boundary. 

  Args:
      f (npt.NDArray[np.float64]): Function
      x0 (int): x coordinate
      y0 (int): y coordinate

  Returns:
      np.float64: Value of the laplacian at point (x0, y0) for function f.
  """
  center = f[x0, y0]
  left = center if x0 == 0 else f[x0 - 1, y0]
  right = center if x0 == SIZE_X - 1 else f[x0 + 1, y0]
  top = center if y0 == 0 else f[x0, y0 - 1]
  bottom = center if y0 == SIZE_Y - 1 else f[x0, y0 + 1]

  # laplacian components of each dimension
  d2fdx2 = (left - 2 * center + right) / DX**2
  d2fdy2 = (top - 2 * center + bottom) / DY**2
  return d2fdx2 + d2fdy2

for t in tqdm(range(T - 1)):
  for x in range(SIZE_X):
    for y in range(SIZE_Y):
      # Note: for overall quantity of elements to stay constant the coefficients in front of
      # c1 * c2 must sum to 0 (K1 + K2 + K3 = 0)
      c1c2 = c1[x, y, t] * c2[x, y, t]
      c1[x, y, t + 1] = c1[x, y, t] + K1 * DT * c1c2 + DT * D * laplacian(c1[:, :, t], x, y)
      c2[x, y, t + 1] = c2[x, y, t] + K2 * DT * c1c2 + DT * D * laplacian(c2[:, :, t], x, y)
      c3[x, y, t + 1] = c3[x, y, t] + K3 * DT * c1c2

c = np.stack((c1, c2, c3), axis=0)
print(c.shape)
print('Saving results')
filename = simulation_identifier(params, 'npy')
np.save(f'saves/suboptimal/{filename}', c)

# %%
