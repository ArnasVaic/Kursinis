# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from solver_config import *
from initial_config import get_c_init

# %%

# load parameters
W = solver_config['W']
H = solver_config['H']
N = solver_config['N']
M = solver_config['M']
D = solver_config['D']
k = solver_config['k']
c0 = solver_config['c0']

dts = [
  solver.get_upper_dt_bound_from_config(solver_config),
  0.0001
]

# %%
RUNNING_TIME = 80
for dt in dts:
  solver_config['dt'] = dt
  T = int(RUNNING_TIME / dt)
  stride = T // 200
  c_init = get_c_init(N, M, c0=c0)
  t, c = solver.solve(
    W, H, N, M, D, c0, k, *c_init,
    threshold=None, t_mix=None, debug=True,
    T=T, dt=dt,
    frame_stride=stride)

  asset_dir = '../assets/saves/time-error'
  np.save(f'{asset_dir}/{solver_config_id()}.npy', c)
  np.save(f'{asset_dir}/{solver_config_id()}-t.npy', t)

# %%

import numpy as np
import matplotlib.pyplot as plt
from solver_config import *


fig, ax = plt.subplots(1, 3, figsize=(15, 5))
dir = '../assets/saves/time-error'

for i in range(3):
  ax[i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))

markers = [ '+', 'x' ]
colors = [ 'orange', 'blue' ]
for dt_index, dt in enumerate(dts):

  for i in range(3):
    solver_config['dt'] = dt
    c = np.load(f'{dir}/{solver_config_id()}.npy')
    n = np.load(f'{dir}/{solver_config_id()}-t.npy')
    q = c[i].sum(axis=(1, 2)) / (N * M)

    marker_stride = len(n) // 10

    ts = n * dt
    qs = q
    ax[i].plot(ts, qs, linestyle = 'dotted' if dt_index != 0 else None, color=colors[dt_index], zorder=dt_index, lw=3, label=f'$\Delta t = {dt:.4f}$')
    #ax[i].scatter(ts[::marker_stride], qs[::marker_stride], marker=markers[dt_index], label=f'$\Delta t = {dt}$',color=colors[dt_index], zorder=dt_index)

    #ax[i].title.set_text(f'q $c_{i+1}$')

    ax[i].set_xlabel('$n$')
    ax[i].set_ylabel(f'$q_{{{i + 1}, n}}$')

plt.legend()
plt.show()

plt.figure(dpi=300)
# %%
