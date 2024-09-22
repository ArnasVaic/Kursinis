# %%

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

c = np.load(f'saves/optimized/[n,t,cs]=[100,10000,0]-optimized.npy')
c1, c2, c3 = c[0], c[1], c[2]

SIZE_X, SIZE_Y, T = c.shape[1:]
print(SIZE_X, SIZE_Y, T)

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
# %%
