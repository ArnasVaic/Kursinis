# %%

import numpy as np
import matplotlib.pyplot as plt
import solver

# plt font
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# solver configuration for a reaction without mixing
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
  'optimal_mix': True
}

dt = solver.get_upper_dt_bound_from_config(solver_config)

# run simulation without mixing
t0, _ = solver.solvec(solver_config, debug=False)
t_end = t0[-1] * dt
print(f"Reaction end time (no mixing): {t_end}")

# run simulation with mixing (at different times)

sample_size = 20

ts_mix = 3600 * np.arange(0.99, 9.99, 1)

for t_mix in ts_mix:

    solver_config['t_mix'] = t_mix

    t_mix_end_avg = 0

    for i in range(sample_size):
        t, _ = solver.solvec(solver_config, debug=False)
        t_mix_end_avg = t_mix_end_avg + t[-1] * dt / sample_size

    print(f"Reaction average end time (with mixing): {t_mix_end_avg}")
# %%

# run simulation with optimal mixing (at different times)
ts_mix = 3600 * np.arange(0.99, 9.99, 1)

for t_mix in ts_mix:
    solver_config['t_mix'] = t_mix
    t, _ = solver.solvec(solver_config, debug=False)
    print(f"Reaction end time (optimal mixing): {t[-1] * dt}")