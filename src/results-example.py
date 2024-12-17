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
t = np.load(f'../assets/saves/T-{id}.npy')
T, N, M = c.shape[1:]

c0 = solver_config['c0']
frame_stride = solver_config['frame_stride']

dt = get_upper_dt_bound_from_config(solver_config)

vmax = [ 3 * c0, 5 * c0, c[2].max() ]


# %%
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

def index_of_nearest(array, value):
  array = np.asarray(array)
  return (np.abs(array - value)).argmin()

FIG_HEIGHT, FIG_CNT = 3, 4
FIG_SIZE = (FIG_CNT * FIG_HEIGHT, FIG_HEIGHT)

# timestamps to visualize (hours)
timestamps = np.array([ 0.0, 0.9, 1.01, 1.5 ])

assert len(timestamps) == FIG_CNT

# need to convert to time-steps
time_steps = [ index_of_nearest(t * dt, 3600 * ts) for ts in timestamps ]

plt.figure(dpi=300)
color_map = plt.get_cmap('inferno')

# chose material index for visualization
for element_id in range(3):
  
  fig, ax = plt.subplots(1, FIG_CNT, figsize=FIG_SIZE)

  for index, strided_step in enumerate(time_steps):
  
    axis = ax.flat[index]

    # actual step
    step = t[strided_step]

    # set y label on the first figure
    if index == 0:
      axis.set_ylabel(f'$c_{element_id+1}$', fontsize=16)

    # convert title to hours
    total_minutes = int(step * dt / 60)
    hrs = total_minutes // 60
    min = total_minutes % 60
    title = f'$t=${hrs}h {min}min'
    axis.set_title(title, fontsize=16)

    ticks = ticker.MaxNLocator(2)

    # Set the yaxis major locator using your ticker object. You can also choose the minor
    # tick positions with set_minor_locator.
    axis.yaxis.set_major_locator(ticks)
    axis.xaxis.set_major_locator(ticks)

    # transpose and flip
    img = np.flip(c[element_id, strided_step].T, axis=1)
    cc = axis.imshow(
      img,
      cmap=color_map,
      extent = [0, 1, 1, 0],
      origin='upper',
      vmin=0,
      vmax=vmax[element_id])

  normalizer = Normalize(0, vmax[element_id])
  im = cm.ScalarMappable(norm=normalizer)
  fig.colorbar(cc, ax=ax.ravel().tolist())
  plt.savefig(f'random-mix-example-c{element_id}.pdf')

# %%
