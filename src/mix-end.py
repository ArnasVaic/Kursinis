# %%
import numpy as np
import matplotlib.pyplot as plt
import solver
from scipy.interpolate import interp1d
from solver_config import *

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

# iterate through different mix times
# see how reaction end time depends on it

# 3600 because we want to specify in hours
# but the model time is in seconds
ts_mix = 3600 * np.concatenate((
    np.arange(0, 3.8, 0.2),
    np.arange(4, 11, 0.5)
))

ts_end = np.zeros(ts_mix.shape)

# %%
for index, t_mix in enumerate(ts_mix):
    print(f"t_mix = {t_mix} [{index + 1}/{len(ts_mix)}]")
    solver_config['t_mix'] = [ t_mix ]

    t, _ = solver.solvec(solver_config)
    ts_end[index] = t[-1] * dt

np.save('../assets/saves/mix-end-large-random.npy', ts_end)

# %%

solver_config['t_mix'] = None 
t_nomix, _ = solver.solvec(solver_config)
ts_nomix_end = np.repeat(t_nomix[-1] * dt, ts_mix.shape)

def to_time_string(t_sec):
    t_min = int(t_sec / 60)
    hrs, min = t_min // 60, t_min % 60
    return f"${hrs}h\, {min}min$"

plt.figure(figsize=(5, 4), dpi=300)
ts_end = np.load('../assets/saves/mix-end-large-random.npy')

ts_mix_new = np.linspace(ts_mix.min(), ts_mix.max(), 300)
ts_end_smooth = interp1d(ts_mix, ts_end, kind='cubic')

low = ts_mix[np.argmin(ts_end)] - 0.5

#plt.gca().set_ylim([low/3600 - 0.5, t_nomix / 3600 + 0.5])
plt.xlabel('$t_\\text{mix}\quad[h]$')
plt.ylabel('$t_\\text{end}\quad[h]$')

t_nomix_timestr = to_time_string(t_nomix[-1] / 60)
t_opt_timestr = to_time_string(np.min(ts_end))

plt.plot(
    ts_mix / 3600,
    ts_end / 3600)
plt.plot(
    ts_mix / 3600,
    ts_nomix_end / 3600,
    label=f"Reakcijos pabaigos\nlaikas be išmaišymo",
    linestyle="dashed")
plt.scatter([ts_mix[np.argmin(ts_end)] / 3600], np.min(ts_end) / 3600, label=f"Trumpiausias įmanomas\nreakcijos laikas")
plt.legend()
plt.tight_layout()
plt.savefig("mix-end.pdf")

# %%
