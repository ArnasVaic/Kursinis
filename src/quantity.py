# %%
import numpy as np
import matplotlib.pyplot as plt
import solver

# pretty font
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

solver_config = {

  # frame stride
  'frame_stride': 10,

  # time step
  'dt': None,

  # reaction parameters
  'W': 2 * 2.154434690031884,
  'H': 2 * 2.154434690031884,
  'N': 2 * 80,
  'M': 2 * 80,
  'D': 28e-6,
  'k': 192,
  'c0': 1e-6,
  
  # stop condition
  'threshold': 0.03,
  'T': None,
  
  # mixing parameters
  'B': 4,
  't_mix': None,
  'optimal_mix': True,
}

dt = solver.get_upper_dt_bound_from_config(solver_config)

t, c = solver.solvec(solver_config)

solver_config['t_mix'] = [ 0 * 3600 ]

t_mixed, c_mixed = solver.solvec(solver_config)

W, H = solver_config['W'], solver_config['H'] 
T, N, M = c[2].shape
t_mix = solver_config['t_mix']

q = np.sum(c[2], axis=(1, 2)) * W * H / (N * M)
q_mixed = np.sum(c_mixed[2], axis=(1, 2)) * W * H / (N * M)

plt.figure(figsize=(5, 4))
plt.title('Trečios medžiagos $c_3$ kiekio priklausomybė nuo laiko')
plt.xlabel('$t\quad[h]$')
plt.ylabel('$q\quad[g]$')

plt.plot(t_mixed * dt / 3600, q_mixed, label=f'$q(t)$ su maišymu')
plt.plot(t * dt / 3600, q, label=f'$q(t)$ be maišymo')

plt.scatter(
    np.array(t_mix) / 3600, 
    [ q[ int( T * tm / (t[-1] * dt) ) ] for tm in t_mix ], 
    label='$t^1_{mix}=3h$')

plt.legend()
plt.tight_layout()
plt.savefig('optimal-mix-qnt.pdf')
 # %%
