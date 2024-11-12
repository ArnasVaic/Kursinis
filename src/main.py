# %%
import numpy as np
from solver_config import *
import matplotlib.pyplot as plt
from initial_config import *
from solver import *

W, H = solver_config['W'], solver_config['H']
dx, dy = solver_config['dx'], solver_config['dy']
c0 = solver_config['c0']
k = solver_config['k']
D = solver_config['D']
B = solver_config['B']
t_mix = solver_config['t_mix']

N, M = int(W / dx) + 1, int(H / dy) + 1

c1_init, c2_init = setup_initial_c1c2(N, M, c0)
c = solve(W, H, N, M, D, c0, k, c1_init, c2_init, threshold=0.03, debug=True)

# skip as many frames as needed
# to keep file sizes small and 
# frame count around 200
stride = max(1, int(c.shape[1] / 200))
c = c[:, ::stride, :, :]

print(f'stride: {stride}')
solver_config['out_stride'] = stride

np.save(f'../assets/saves/{solver_config_id()}.npy', c)
# %%
