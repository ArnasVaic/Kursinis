# %%
import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
from solver import get_dt

id = solver_config_id()
c1, c2, c3 = np.load(f'saves/{id}.npy')
dx, dy = solver_config['dx'], solver_config['dy']
D = solver_config['D']

dt = get_dt(dx, dy, D, c1[0].max(), c2[0].max())

T, N, M = c3.shape
q = np.sum(c3, axis=(1, 2))

ts = np.linspace(0, T * dt, T)
plt.title(f'Medžiagos $c_3$ kiekio $q$ priklausomybė nuo laiko.')
plt.xlabel('$t$')
plt.ylabel('q')
plt.plot(ts, q, label=f'$q(t)=\\sum_{{i=0}}^{{N-1}}\\sum_{{j=0}}^{{M-1}}c_3(i, j, t)$')
plt.legend()
 # %%
