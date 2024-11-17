# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from solver_config import *
from initial_config import get_c_init

# cache calculations
c0 = solver_config['c0']
dt = solver_config['dt']

for s in [20, 10]:
  c_init = get_c_init(N=s, M=s, c0=c0)

  solver_config['N'] = s
  solver_config['M'] = s

  t, c = solver.solve(
    1.0,
    1.0,
    s,
    s,
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

  dir = '../assets/saves/space-error'
  np.save(f'{dir}/{solver_config_id()}.npy', c)
  np.save(f'{dir}/{solver_config_id()}-t.npy', t)

# %%

import numpy as np
import matplotlib.pyplot as plt
from solver_config import *


fig, ax = plt.subplots(1, 3, figsize=(15, 5))
dt = solver_config['dt']
dir = '../assets/saves/space-error'

for i in range(3):
  ax[i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))

#plots = [None, None, None]
#for i in range(3):  

# fig.suptitle(f'Medžiagų kiekio priklausomybė nuo laiko')

for s in [80, 40, 20, 10]:
  for i in range(3):

    solver_config['N'] = s
    solver_config['M'] = s

    c = np.load(f'{dir}/{solver_config_id()}.npy')
    n = np.load(f'{dir}/{solver_config_id()}-t.npy')
    q = c[i].sum(axis=(1, 2)) / (s ** 2)
    ax[i].plot(n, q, label=f'$N = M = {s}$')

    #ax[i].title.set_text(f'q $c_{i+1}$')

    ax[i].set_xlabel('$n$')
    ax[i].set_ylabel(f'$q_{{{i + 1}, n}}$')

plt.legend()
plt.show()

plt.figure(dpi=300)
# %%
