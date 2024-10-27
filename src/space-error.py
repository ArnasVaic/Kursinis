# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from initial_config import setup_initial_c1c2

D = 0.0001
T = 2000
dt = 0.01

stride = 5

plt.figure(dpi=300)

for s in [80, 60, 40]:

  N = M = s

  c1, c2 = setup_initial_c1c2(N, M)
  c = solver.solve(
    1, 1, N, M, D,
    c1, c2, T=T, dt=dt,
    debug=True
  )

  q = c[2, ::stride, :, :].sum(axis=(1, 2)) / (N * M)
  ts = np.linspace(0, T * dt, q.shape[0])
  plt.plot(ts, q, label=f'$(N,M)=({s},{s})$')

plt.title(f'Medžiagos kiekio $c_3$ priklausomybė nuo laiko.\n$T={T},dt={dt},D={D}$')
plt.xlabel('$t$')
plt.ylabel('$\\frac{q(t)}{N*M}$')
plt.legend()
plt.show()