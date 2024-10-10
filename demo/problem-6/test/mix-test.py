# %% 
import numpy as np

import os
import sys
# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

from mixer import mix

a = np.reshape(np.arange(4**2), shape=(4, 4))
b = np.roll(a, 1, axis=0)
c = np.roll(b, -1, axis=1)
A, B, C = mix([a, b, c])
#a, b, c, A, B, C
[print(m) for m in [a, b, c, A, B, C]]
# %%
