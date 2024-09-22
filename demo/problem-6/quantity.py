# %%

import numpy as np
import matplotlib.pyplot as plt
import configparser
from simid import simulation_identifier

config = configparser.ConfigParser() 
config.read('simulation-parameters.ini')
params = config['DEFAULT']

filename = simulation_identifier(params, 'npy')
c = np.load(f'saves/optimized/{filename}')
c1, c2, c3 = c[0], c[1], c[2]

T = int(params['T'])
DX = float(params['DX'])
DY = float(params['DY'])
D = float(params['D'])
# DT size depends on the maximum c1/c2 value
DT1 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 3 * np.max(c2[:, :, 0]))
DT2 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 5 * np.max(c1[:, :, 0]))
DT = np.min([DT1, DT2])

SIZE_X, SIZE_Y, T = c.shape[1:]

c1_quantity = np.sum(c1, axis=(0, 1))
c2_quantity = np.sum(c2, axis=(0, 1))
c3_quantity = np.sum(c3, axis=(0, 1))

ts = np.linspace(0, T * DT, T)
plt.title(f'Quantity of elements $c_1$, $c_2$, $c_3$ over time.\n Configuration: {simulation_identifier(params)}')
plt.xlabel('t')
plt.ylabel('$c_1$, $c_2$, $c_3$ quantity')
plt.plot(ts, c1_quantity, label=f'$c_1$')
plt.plot(ts, c2_quantity, label=f'$c_2$')
plt.plot(ts, c3_quantity, label=f'$c_3$')
plt.plot(ts, c1_quantity + c3_quantity + c2_quantity, label=f'$\\Sigma c_i$')
plt.legend(loc='upper left')
 # %%
