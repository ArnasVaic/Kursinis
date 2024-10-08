# %%
import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
from solver import *

W, H, D = 1, 1, 0.01
M = 30
dy = H / (M - 1)

plt.title(
f"""Medžiagos kiekio $c_3$ priklausomybės nuo laiko\n
gautos Oilerio metodu su skirtingais žingsniais $\\Delta x$\n
kiti parametrai bendri $\\Delta y=\\frac{{{H}}}{{{M-1}}},D={D}$""")
plt.xlabel('$t$')
plt.ylabel('$q(t)$')
for N in [40, 30, 20, 10]:
  dx = W / (N - 1)
  c = np.load(f'saves/[N,M,D]=[{N},{M},{D}].npy')
  T = c.shape[1]
  dt = get_dt(dx, dy, D, c[0, 0].max(), c[1, 0].max())
  ts = np.linspace(0, T * dt, T)
  plt.plot(ts, c[2].sum(axis=(1, 2)), label=f'$\\Delta x=\\frac{{{W}}}{{{N-1}}}$')
plt.legend()
# %%
