# %%

import numpy as np
from tqdm import tqdm
from scipy.signal import convolve2d

# Simulation configurations
L, T = 1, 10000
DX, DY = 0.01, 0.01
# Thermal diffusivity α (alpha)
D = 1/4

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

# Convolving with this kernel gives laplacian
ONE_OVER_DX2 = 1 / DX**2
ONE_OVER_DY2 = 1 / DY**2
DIFF_KERNEL = np.array([
  [0, ONE_OVER_DY2, 0],
  [ONE_OVER_DX2, -2 * ( ONE_OVER_DX2 + ONE_OVER_DY2 ), ONE_OVER_DX2],
  [0, ONE_OVER_DY2, 0]
])

def laplacian(c):
  padded = np.pad(c, (1, 1), 'edge')
  return convolve2d(padded, DIFF_KERNEL, mode='valid')

for t in tqdm(range(T - 1)):
  # Note: for overall quantity of elements to stay constant the coefficients
  # in front of c1c2 should sum to 0
  c1[:, :, t + 1] = c1[:, :, t] + DT * D * laplacian(c1[:, :, t]) - 3 * DT * c1[:, :, t] * c2[:, :, t]
  c2[:, :, t + 1] = c2[:, :, t] + DT * D * laplacian(c2[:, :, t]) - 5 * DT * c1[:, :, t] * c2[:, :, t]
  c3[:, :, t + 1] = c3[:, :, t] + 8 * c1[:, :, t] * c2[:, :, t] * DT

c = np.stack((c1, c2, c3), axis=0)
print(c.shape)
np.save(f'saves/optimized/[n,t,cs]=[{SIZE_X},{T},0]-optimized.npy', c)
# %%
