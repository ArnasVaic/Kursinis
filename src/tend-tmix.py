# %%

import matplotlib.pyplot as plt
from solver_config import *
from solver import *

ts_mix, ts_end = np.load('saves/mix-times.npy').T
#ts_mix, ts_end = ts_mix.squeeze(), ts_end.squeeze()
print(ts_mix.shape, ts_end.shape)

colors =  plt.cm.get_cmap('turbo', len(ts_mix))
color_list = [colors(i) for i in range(len(ts_mix))]

plt.title(
"""Medžiagų $c_1$ ir $c_2$ reakcijos pabaigos 
laiko $t_{end}$ priklausomybė nuo maišymo laiko $t_{mix}$""")
plt.gca().set_ylim((ts_end.min() - 100, ts_end.max() + 100))
plt.xlabel('$t_{mix}$')
plt.ylabel('$t_{end}$')
plt.plot(ts_mix, ts_end)
# %%
