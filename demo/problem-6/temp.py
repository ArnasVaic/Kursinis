# %%
import numpy as np
from mixer import mix

a = np.eye(8, 8)
mix([a], rotate=True, shuffle=False, subdivisions=(2, 2), debug=False)
# %%
