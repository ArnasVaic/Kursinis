# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from solver_config import *

t, c = solver.solvec(solver_config, debug=True)

dir = '../assets/saves'
np.save(f'{dir}/{solver_config_id()}.npy', c)
np.save(f'{dir}/{solver_config_id()}-t.npy', t)

# %%

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

dir = '../assets/saves'
c = np.load(f'{dir}/{solver_config_id()}.npy')
t = np.load(f'{dir}/{solver_config_id()}-t.npy')

N = solver_config['N']
M = solver_config['M']
dt = solver.get_upper_dt_bound_from_config(solver_config)

plt.figure(dpi=1200)
for i in range(3):
    q_i = c[i].sum(axis=(1,2)) / (N * M)
    plt.plot(t * dt / 3600, q_i, label=f'$q_{{{i+1}, n}}$')
plt.xlabel('$t\\quad [h]$')
plt.ylabel('$q\\quad [g]$')
plt.legend(bbox_to_anchor=(1, 0.5))
plt.savefig('only-diff.pdf')
# %%
