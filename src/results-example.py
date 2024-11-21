# %%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from solver_config import *
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from solver import get_upper_dt_bound_from_config

id = solver_config_id()
c = np.load(f'../assets/saves/{id}.npy')
t = np.load(f'../assets/saves/{id}-t.npy')
T, N, M = c.shape[1:]

c0 = solver_config['c0']

dt = get_upper_dt_bound_from_config(solver_config)

vmax = [ 3 * c0, 5 * c0, 1 ]


# %%
# chose material index for visualization
for c_id in [0, 1, 2]:

  print(f'T = {T}')

  plt.figure(dpi=300)
  fig_h = 5
  figs = 5
  fig, ax = plt.subplots(1, figs, figsize=(figs * fig_h, fig_h))

  cmap = plt.get_cmap('inferno')

  ns = [0, 4, 25, 75, 201]

  assert len(ns) == figs

  for i, n in enumerate(ns):

    # if i == 2:
    #   ax.flat[i].set_xlabel(f'$x$', labelpad=0)
    
    if i == 0:
      ax.flat[i].set_ylabel(f'$c_{c_id+1}$', fontsize=16)

    ax.flat[i].set_title(f'$t={n * dt:.4f}$', fontsize=16)

    ticks = ticker.MaxNLocator(2)

    # Set the yaxis major locator using your ticker object. You can also choose the minor
    # tick positions with set_minor_locator.
    ax[i].yaxis.set_major_locator(ticks)
    ax[i].xaxis.set_major_locator(ticks)

    cc = ax.flat[i].imshow(
      np.flip(c[c_id, n].T, axis=1),
      cmap=cmap,
      extent = [0, 1, 1, 0],
      origin='upper',
      vmin=0,
      vmax=vmax[c_id])

  normalizer = Normalize(0, vmax[c_id])
  im = cm.ScalarMappable(norm=normalizer)
  fig.colorbar(cc, ax=ax.ravel().tolist())
  plt.show()

# %%
