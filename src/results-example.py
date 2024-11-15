# %%

import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from solver import get_upper_dt_bound_from_config

id = solver_config_id()
c = np.load(f'../assets/saves/{id}.npy')
t = np.load(f'../assets/saves/T-{id}.npy')
T, N, M = c.shape[1:]

c0 = solver_config['c0']

dt = get_upper_dt_bound_from_config(solver_config)

# chose material index for visualization
c_id = 0

vmax = [ 3 * c0, 5 * c0, c[2, -1].max() ]

print(f'T = {T}')

plt.figure(dpi=1200)
fig_h = 6
figs = 5
fig, ax = plt.subplots(1, figs, figsize=(figs * fig_h, fig_h))

cmap = plt.get_cmap('inferno')

ns = [0, 2, 6, 15, 31]

assert len(ns) == figs

for i, n in enumerate(ns):

  ax[i].set_xlabel(f'$x$')

  ax[i].set_ylabel(f'$y$')

  ax[i].title.set_text(f'Medžiagos $c_{c_id+1}$ koncentracija\n laiko momentu $n={n * dt:04f}$')

  cc = ax[i].imshow(
    np.flip(c[c_id, n].T, axis=1),
    cmap=cmap,
    extent = [0, 1, 1, 0],
    origin='upper',
    vmin=0, 
    vmax=vmax[c_id])

normalizer = Normalize(0, vmax[c_id])
im = cm.ScalarMappable(norm=normalizer)
fig.colorbar(cc, ax=ax.ravel().tolist())

#fig.tight_layout()
plt.show()

# %%
