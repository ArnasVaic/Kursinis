# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from solver_config import *
from initial_config import get_c_init

N = solver_config['N']
M = solver_config['M']
c0 = solver_config['c0']

c_init = get_c_init(N, M, c0)

# generate data
t, c = solver.solve(
    solver_config['W'], solver_config['H'],
    N, M,
    solver_config['D'], solver_config['c0'], solver_config['k'],
    *c_init,
    T=solver_config['T'],
    dt=solver_config['dt'],
    debug=True,
    frame_stride=solver_config['frame_stride'])

dir = '../assets/saves'
np.save(f'{dir}/{solver_config_id()}.npy', c)
np.save(f'{dir}/{solver_config_id()}-t.npy', t)

# %%

dir = '../assets/saves'
c = np.load(f'{dir}/{solver_config_id()}.npy')
t = np.load(f'{dir}/{solver_config_id()}-t.npy')

N = solver_config['N']
M = solver_config['M']
dt = solver_config['dt']

plt.figure(dpi=1200)
for i in range(3):
    q_i = c[i].sum(axis=(1,2)) / (N * M)
    plt.plot(t * dt, q_i, label=f'$q_{i+1}$')
plt.xlabel('$t$')
plt.ylabel('$q$')
plt.legend(bbox_to_anchor=(1, 0.5))
# %%
