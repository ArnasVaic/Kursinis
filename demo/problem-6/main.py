# %%
import numpy as np
from solver_config import *
import matplotlib.pyplot as plt
from solver import *

W, H = solver_config['W'], solver_config['H']
dx, dy = solver_config['dx'], solver_config['dy']
D = solver_config['D']
t_mix = solver_config['t_mix']

w, h = int(W / dx) + 1, int(H / dy) + 1
hw, hh = int(w/2), int(h/2)

# Initial conditions at t = 0: 4 non-overlapping blocks
c1, c2 = np.zeros((w, h)), np.zeros((w, h))
c1[:hw, :hh] = c1[hw:, hh:] = 3 * 200 / ( w * h )
c2[hw:, :hh] = c2[:hw, hh:] = 5 * 200 / ( w * h )

print(f"c1 cell value: {c1[0,0]}, q1(0) = {c1.sum()}")
print(f"c2 cell value: {c2[-1,0]}, q2(0) = {c2.sum()}")

c = solve(W ,H, dx, dy, D, c1, c2, 0.02, t_mix, True)

# skip as many frames as needed
# to keep file sizes small and 
# frame count around 200
stride = max(1, int(c.shape[1] / 200))
c = c[:, ::stride, :, :]

check_solution(c)

print(f'stride: {stride}')
solver_config['out_stride'] = stride

np.save(f'saves/{solver_config_id()}.npy', c)
# %%
