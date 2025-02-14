# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from solver_config import *
from initial_config import get_c_init

# cache calculations
c0 = solver_config['c0']
dt = solver_config['dt']

for s in [80, 40, 20, 10]:
  c_init = get_c_init(N=s, M=s, c0=c0)

  solver_config['N'] = s
  solver_config['M'] = s

  t, c = solver.solvec(solver_config, debug=True)

  dir = '../assets/saves/space-error'
  np.save(f'{dir}/{solver_config_id()}.npy', c)
  np.save(f'{dir}/{solver_config_id()}-t.npy', t)

# %%

import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

plt.figure(dpi=1200)

fig, ax = plt.subplots(1, 3, figsize=(9, 3))
dir = '../assets/saves/space-error'

ax[1].set_xlabel('$t\quad [h]$')
ax[0].set_ylabel('$q\quad [g]$')

for s in [80, 40, 20, 10]:
  for i in range(3):

    solver_config['N'] = s
    solver_config['M'] = s

    dt = solver.get_upper_dt_bound_from_config(solver_config)

    c = np.load(f'{dir}/{solver_config_id()}.npy')
    t = np.load(f'{dir}/{solver_config_id()}-t.npy')
    q = c[i].sum(axis=(1, 2)) / (s ** 2)
    ax[i].plot(t * dt / 3600, q, label=f'$N = M = {s}$')
    
    ax[i].set_title(f'Medžiagos $c_{{{i + 1}}}$ kiekio\npriklausomybė nuo laiko')

plt.legend()
plt.tight_layout()
plt.savefig('space-error.pdf')
# %%
