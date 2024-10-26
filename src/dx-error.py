# %%
%reload_ext autoreload
%autoreload 2
import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
import solver
from initial_config import *
from tqdm import tqdm

import importlib
importlib.reload(solver)

W, H, D = 1, 1, 0.0001
M = 30

plt.title(
f"""Medžiagos kiekio $c_3$ priklausomybės nuo laiko\n
gautos Oilerio metodu su skirtingais žingsniais $\\Delta x$\n
kiti parametrai bendri $M={M},D={D}$""")
plt.xlabel('$t$')
plt.ylabel('$q(t)$')

T = 3
stride = max(1, int(T / 200))
dt = 0.00004

# all had different amounts of initial 
for N in [10, 20, 50, 98, 100]:

  c1_init, c2_init = setup_initial_c1c2(N, M)

  c = solver.solve(
    W, H, N, M, D,
    c1_init, c2_init, 
    T = T, dt=dt,
    threshold=0.02, t_mix=None, 
    debug=True)
  
  solver.validate_solution(c)
  
  q = c[2, ::stride, :, :].sum(axis=(1, 2))
  ts = np.linspace(0, T * dt, q.shape[0])
  plt.plot(ts, q, label=f'$N={N}$')

plt.legend()
#  %%
