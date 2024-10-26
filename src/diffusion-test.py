# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
import initial_config

N, M = 20, 20
T = 1000
dt = 0.01

c1 = np.reshape(np.repeat(1, N * M), (N, M))
c2 = np.zeros((N, M))
print(c2)

c = solver.solve(
  1, 1, N, M,
  0.0001,
  c1,
  c2,
  T=T,
  dt=dt,
  debug=True
)

solver.validate_solution(c)

q = c[2, ::5, :, :].sum(axis=(1, 2))
ts = np.linspace(0, T * dt, q.shape[0])
plt.plot(ts, q, label=f'$N={N}$')

# %%
