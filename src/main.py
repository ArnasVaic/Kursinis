# %%
import numpy as np
from solver_config import *
from initial_config import *
from solver import *

t, c = solvec(solver_config, True)

np.save(f'../assets/saves/{solver_config_id()}.npy', c)
np.save(f'../assets/saves/T-{solver_config_id()}.npy', t)
# %%
