# %%
import numpy as np
import matplotlib.pyplot as plt
from solver_config import *
from solver import *
from initial_config import *
from tqdm import tqdm

W, H, D = 1, 1, 0.0001
M = 30
dy = H / (M - 1)

plt.title(
f"""Medžiagos kiekio $c_3$ priklausomybės nuo laiko\n
gautos Oilerio metodu su skirtingais žingsniais $\\Delta x$\n
kiti parametrai bendri $\\Delta y=\\frac{{{H}}}{{{M-1}}},D={D}$""")
plt.xlabel('$t$')
plt.ylabel('$q(t)$')
for N in tqdm([40, 36, 28, 24, 20, 16, 10]):
  dx = W / (N - 1)
  c1_init, c2_init = setup_initial_c1c2(N, M)
  c = solve(W, H, dx, dy, D, c1_init, c2_init, 0.02, None)
  check_solution(c)
  T = c.shape[1]
  stride = max(1, int(c.shape[1] / 200))
  c1, c2, c3 = c[:, ::stride, :, :]
  dt = get_dt(dx, dy, D, c1_init.max(), c2_init.max())
  ts = np.linspace(0, T * dt, c3.shape[0])
  q = c3.sum(axis=(1, 2))
  plt.plot(ts, q, label=f'$\\Delta x=\\frac{{{W}}}{{{N-1}}}$')
plt.legend()
# %%
