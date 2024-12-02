# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from solver_config import *
from initial_config import get_c_init

# %%

# cache calculations
c0 = solver_config['c0']
N = solver_config['N']
M = solver_config['M']

for dt in [0.05, 0.01, 0.001, 0.0001]:
  solver_config['dt'] = dt
  c_init = get_c_init(N, M, c0=c0)
  t, c = solver.solve(
    1.0,
    1.0,
    N,
    M,
    solver_config['D'],
    c0,
    solver_config['k'],
    *c_init,
    threshold=None,
    t_mix=None,
    debug=True,
    T=solver_config['T'],
    dt=dt,
    frame_stride=solver_config['frame_stride'])

  dir = '../assets/saves/time-error'
  np.save(f'{dir}/{solver_config_id()}.npy', c)
  np.save(f'{dir}/{solver_config_id()}-t.npy', t)

# %%

import numpy as np
import matplotlib.pyplot as plt
from solver_config import *


fig, ax = plt.subplots(1, 3, figsize=(15, 5))
dir = '../assets/saves/time-error'

for i in range(3):
  ax[i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))

for dt in [0.05, 0.01, 0.001, 0.0001]:
  for i in range(3):
    solver_config['dt'] = dt
    c = np.load(f'{dir}/{solver_config_id()}.npy')
    n = np.load(f'{dir}/{solver_config_id()}-t.npy')
    q = c[i].sum(axis=(1, 2)) / (N * M)
    ax[i].plot(n * dt, q, label=f'$\Delta t = {dt}$')

    #ax[i].title.set_text(f'q $c_{i+1}$')

    ax[i].set_xlabel('$n$')
    ax[i].set_ylabel(f'$q_{{{i + 1}, n}}$')

plt.legend()
plt.show()

plt.figure(dpi=300)
# %%
