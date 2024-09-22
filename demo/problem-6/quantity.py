# %%

import numpy as np
import matplotlib.pyplot as plt

c = np.load(f'saves/suboptimal/[n,t,cs]=[10,100,0].npy')
c1, c2, c3 = c[0], c[1], c[2]

SIZE_X, SIZE_Y, T = c.shape[1:]
print(SIZE_X, SIZE_Y, T)

c1_quantity = np.sum(c1, axis=(0, 1))
c2_quantity = np.sum(c2, axis=(0, 1))
c3_quantity = np.sum(c3, axis=(0, 1))

ts = np.arange(0, T, 1)
plt.title(f'Quantity of elements $c_1$, $c_2$, $c_3$ over time.\n Configuration: [n, t, cs]=[{SIZE_X}, {T}, 0]')
plt.xlabel('t')
plt.ylabel('$c_1$, $c_2$, $c_3$ quantity')
plt.plot(ts, c1_quantity, label=f'$c_1$')
plt.plot(ts, c2_quantity, label=f'$c_2$')
plt.plot(ts, c3_quantity, label=f'$c_3$')
plt.plot(ts, c1_quantity + c3_quantity + c2_quantity, label=f'$\Sigma c_i$')
plt.legend(loc='upper left')
 # %%
