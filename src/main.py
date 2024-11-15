# %%
import numpy as np
from solver_config import *
import matplotlib.pyplot as plt
from initial_config import *
from solver import *

N, M = solver_config['N'], solver_config['M']
c0 = solver_config['c0']
c_init = get_c_init(N, M, c0)
t, c = solvec(solver_config, c_init, 0.03, True)
np.save(f'../assets/saves/{solver_config_id()}.npy', c)
np.save(f'../assets/saves/T-{solver_config_id()}.npy', t)
# %%
