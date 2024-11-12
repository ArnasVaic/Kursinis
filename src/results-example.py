# %%

import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
from solver import get_upper_dt_bound

id = solver_config_id()
c1, c2, c3 = np.load(f'../assets/saves/{id}.npy')
T, N, M = c3.shape

plt.figure(dpi=1200)
fig, ax = plt.subplots(1, 3, figsize=(15, 5))

cmap = 'viridis'

cc1 = ax[0].imshow(
    c1[0], 
    cmap=cmap, 
    extent = [0, 1, 1, 0],
    origin='upper')

fig.colorbar(cc1, ax=ax[0])

# ax[1].imshow(
#     c1[1], 
#     cmap=cmap,
#     extent = [1, 0, 1, 0])

# ax[2].imshow(
#     c1[-1], 
#     cmap=cmap,
#     extent = [1, 0, 1, 0])


fig.tight_layout()
plt.show()

# %%
