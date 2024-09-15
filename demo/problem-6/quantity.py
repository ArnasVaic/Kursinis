# %%

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

L = 1
SIZE_X, SIZE_Y, T = 10, 10, 100

c1 = np.load(f'saves/c1_{SIZE_X}x{SIZE_Y}_t{T}.npy')
c2 = np.load(f'saves/c2_{SIZE_X}x{SIZE_Y}_t{T}.npy')
c3 = np.load(f'saves/c3_{SIZE_X}x{SIZE_Y}_t{T}.npy')

c1_quantity = np.sum(c1, axis=(0, 1))
c2_quantity = np.sum(c2, axis=(0, 1))
c3_quantity = np.sum(c3, axis=(0, 1))

ts = np.arange(0, T, 1)
plt.title(f'Quantity of elements c1, c2, c3 over time')
plt.xlabel('t')
plt.ylabel('c1, c2, c3 quantity')
plt.plot(ts, c1_quantity, label=f'c1')
plt.plot(ts, c2_quantity, label=f'c2')
plt.plot(ts, c3_quantity, label=f'c3')
plt.plot(ts, c1_quantity + c3_quantity + c2_quantity, label=f'c1 + c2 + c3')
plt.legend()