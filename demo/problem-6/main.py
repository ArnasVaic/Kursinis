# %%

import numpy as np
import numpy.typing as npt

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

def laplacian(
  c: npt.NDArray[np.float64], 
  x: int, 
  y: int, 
  t: int) -> np.float64: 
  # When x,y is on the boundary some
  # of the neighbors will not exist
  # and will need to be chosen specifically
  # to ensure boundary conditions. In this case
  # we want to make it so dc\dn=0, where n is the normal
  # along the boundary so if one of the neighbors goes
  # out of bounds, we set its value to be the same
  # as the current cell c[x, y, t]

  c_center = c[x, y, t]

  # c_{i-1,j}^n
  # left edge has dc\dx = 0, so value 
  # "beyond" border should match c_center
  c_left = c_center if x == 0 else c[x - 1, y, t]

  # u_{i+1,j}^n
  # right edge has dc\dx = 0, so value 
  # "beyond" border should match c_center
  c_right = c_center if x == SIZE_X - 1 else c[x + 1, y, t]

  # c_{i,j+1}^n
  # top edge has dc\dy = 0, so value 
  # "beyond" border should match c_center
  c_top = c_center if y == 0 else c[x, y - 1, t]

  # c_{i,j-1}^n
  # bottom edge has dc\dy = 0, so value 
  # "beyond" border should match c_center
  c_bottom = c_center if y == SIZE_Y - 1 else c[x, y + 1, t]

  # laplacian components of each dimension (to keep line length small)
  lap_x = (c_left - 2 * c_center + c_right) / (DX**2)
  lap_y = (c_top - 2 * c_center + c_bottom) / (DY**2)

  return lap_x + lap_y

for t in range(T - 1):
  for x in range(SIZE_X):
    for y in range(SIZE_Y):
      # Note: for overall quantity of elements to stay constant the coefficients
      # in front of c1c2 should sum to 0
      c1[x, y, t + 1] = c1[x, y, t] + DT * D * laplacian(c1, x, y, t) - 3 * DT * c1[x, y, t] * c2[x, y, t]
      c2[x, y, t + 1] = c2[x, y, t] + DT * D * laplacian(c2, x, y, t) - 5 * DT * c1[x, y, t] * c2[x, y, t]
      c3[x, y, t + 1] = c3[x, y, t] + 8 * c1[x, y, t] * c2[x, y, t] * DT

np.save(f'saves/c1_{SIZE_X}x{SIZE_Y}_t{T}-adjusted-coef.npy', c1)
np.save(f'saves/c2_{SIZE_X}x{SIZE_Y}_t{T}-adjusted-coef.npy', c2)
np.save(f'saves/c3_{SIZE_X}x{SIZE_Y}_t{T}-adjusted-coef.npy', c3)

# %%
