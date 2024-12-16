# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from solver_config import *
from initial_config import get_c_init

dts = [
  solver.get_upper_dt_bound_from_config(solver_config),
  0.1
]

# %%
RUNNING_TIME = 16 * 3600
for dt in dts:

  solver_config['dt'] = dt
  T = int(RUNNING_TIME / dt)
  solver_config['frame_stride'] = T // 200
  solver_config['T'] = T

  t, c = solver.solvec(solver_config, debug=True)

  asset_dir = '../assets/saves/time-error'
  np.save(f'{asset_dir}/{solver_config_id()}.npy', c)
  np.save(f'{asset_dir}/{solver_config_id()}-t.npy', t)

# %%

import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

plt.figure(dpi=300)

N, M = solver_config['N'], solver_config['M']
fig, ax = plt.subplots(1, 3, figsize=(9, 3))
dir = '../assets/saves/time-error'

ax[0].set_ylabel(f'$q \quad [g]$')
ax[1].set_xlabel('$t \quad [h]$')

colors = [ 'orange', 'blue' ]
for dt_index, dt in enumerate(dts):

  for i in range(3):
    axis = ax[i]
    solver_config['dt'] = dt
    c = np.load(f'{dir}/{solver_config_id()}.npy')
    n = np.load(f'{dir}/{solver_config_id()}-t.npy')
    q = c[i].sum(axis=(1, 2)) / (N * M)

    # plot x axis in hours
    ts = n * dt / 3600
    qs = q
    axis.plot(
      ts, qs, 
      linestyle = 'dotted' if dt_index != 0 else None, 
      color=colors[dt_index], 
      zorder=dt_index, 
      lw=3, 
      label=f'$\Delta t = {dt:.4g}s$')
    axis.set_title(f'$q_{{{i + 1}, n}}$')

plt.legend()
plt.tight_layout()
plt.savefig('time-error.pdf')

# %%
