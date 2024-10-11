# %%
# How q(t) depends on B

import numpy as np
from solver_config import *
import matplotlib.pyplot as plt
from solver import *

W, H = solver_config['W'], solver_config['H']
dx, dy = solver_config['dx'], solver_config['dy']
D = solver_config['D']
t_mix = solver_config['t_mix']

w, h = int(W / dx) + 1, int(H / dy) + 1
hw, hh = int(w/2), int(h/2)

# Initial conditions at t = 0: 4 non-overlapping blocks
c1_init, c2_init = np.zeros((w, h)), np.zeros((w, h))
c1_init[:hw, :hh] = c1_init[hw:, hh:] = 3 * 200 / ( w * h )
c2_init[hw:, :hh] = c2_init[:hw, hh:] = 5 * 200 / ( w * h )

dt = get_dt(dx, dy, D, c1_init[0].max(), c2_init[0].max())

for B in [ 2, 3, 4 ]:
  c = solve(W ,H, dx, dy, D, c1_init, c2_init, 0.02, t_mix, B, debug=False)
  check_solution(c)
  
  stride = max(1, int(c.shape[1] / 200))
  T = c.shape[1]
  c1, c2, c3 = c[:, ::stride, :, :]
  q = np.sum(c3, axis=(1, 2))
  ts = np.linspace(0, T * dt, q.shape[0])
  plt.plot(ts, q, label=f'$B={B}$')

title = f'Medžiagos $c_3$ kiekio $q_3(t)=\\sum_{{i=0}}^{{N-1}}\\sum_{{j=0}}^{{M-1}}c_3(i, j, t)$ priklausomybė nuo laiko.'
plt.title(title)
plt.xlabel('$t$')
plt.ylabel('$q_3$')
plt.legend()
plt.show()
# %%
