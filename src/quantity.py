# %%
import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
import solver

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

id = solver_config_id()
c_mix = np.load(f'../assets/saves/{id}-mix.npy')
ts_mix = np.load(f'../assets/saves/T-{id}-mix.npy')

c = np.load(f'../assets/saves/{id}.npy')
ts = np.load(f'../assets/saves/T-{id}.npy')

dt = solver.get_upper_dt_bound_from_config(solver_config)

W, H = solver_config['W'], solver_config['H'] 
T, N, M = c[2].shape
t_mix = solver_config['t_mix']

q = np.sum(c[2], axis=(1, 2)) * W * H / (N * M)
q_mix = np.sum(c_mix[2], axis=(1, 2)) * W * H / (N * M)

plt.title('$q_{3, n}$')
plt.xlabel('$t\quad[h]$')
plt.ylabel('$q\quad[g]$')

# how to get from t_mix to n?
# t_mix \in [0, ]

plt.plot(ts_mix * dt / 3600, q_mix, label=f'$q(t)$ with mixing')
plt.plot(ts * dt / 3600, q, label=f'$q(t)$ without mixing')

plt.scatter(
    np.array(t_mix) / 3600, 
    [ q[ int( T * tm / (ts[-1] * dt) ) ] for tm in t_mix ], 
    label='$t^1_{mix}=1h$')

plt.legend()
plt.show()
 # %%
