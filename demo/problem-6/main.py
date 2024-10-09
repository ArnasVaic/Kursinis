# %%
import numpy as np
from solver_config import *
from solver import solve

W, H = solver_config['W'], solver_config['H']
dx, dy = solver_config['dx'], solver_config['dy']
D = solver_config['D']
t_mix = solver_config['t_mix']

w, h = int(W / dx) + 1, int(H / dy) + 1
hw, hh = int(w/2), int(h/2)

# Initial conditions at t = 0: 4 non-overlapping blocks
c1, c2 = np.zeros((w, h)), np.zeros([w, h])
c1[:hw, :hh] = c1[hw:, hh:] = 5 * 20 / ( w * h )
c2[hw:, :hh] = c2[:hw, hh:] = 3 * 20 / ( w * h )

c = solve(W ,H, dx, dy, D, c1, c2, 0.02, t_mix, True)

# skip as many frames as needed
# to keep file sizes small and 
# frame count around 200
stride = int(c.shape[1] / 200)
c = c[:, ::stride, :, :]

print(f'stride: {stride}')

np.save(f'saves/{solver_config_id()}.npy', c)
# %%
