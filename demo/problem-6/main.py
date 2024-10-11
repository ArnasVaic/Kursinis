# %%
import numpy as np
from solver_config import *
import matplotlib.pyplot as plt
from initial_config import *
from solver import *

W, H = solver_config['W'], solver_config['H']
dx, dy = solver_config['dx'], solver_config['dy']
D = solver_config['D']
B = solver_config['B']
t_mix = solver_config['t_mix']

N, M = int(W / dx) + 1, int(H / dy) + 1
print(N, M)
c1_init, c2_init = setup_initial_c1c2(N, M)
c = solve(W, H, dx, dy, D, c1_init, c2_init, 0.02, t_mix, B, debug=True)

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
