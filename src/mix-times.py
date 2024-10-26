# %%

import numpy as np
from solver_config import *
import matplotlib.pyplot as plt
from solver import *
from tqdm import tqdm
from initial_config import *

W, H = solver_config['W'], solver_config['H']
dx, dy = solver_config['dx'], solver_config['dy']
D = solver_config['D']

N, M = int(W / dx) + 1, int(H / dy) + 1

# Initial conditions at t = 0: 4 non-overlapping blocks
c1_init, c2_init = setup_initial_c1c2(N, M)
dt = get_dt(dx, dy, D, c1_init.max(), c2_init.max())
unmixed_stop_time = 0

def generate_ts_mix(sample_count, padding = (1/20, 1/5)):
    global unmixed_stop_time
    c = solve(W ,H, dx, dy, D, c1_init, c2_init, 0.02, None) 
    unmixed_stop_time = dt * c.shape[1]
    print(f'unmixed stop time {unmixed_stop_time}')
    start = padding[0] * unmixed_stop_time
    end = unmixed_stop_time * (1 - padding[1])
    return np.linspace(start, end, sample_count)

ts_mix = generate_ts_mix(5)

#colors = plt.cm.get_cmap('rainbow', len(ts_mix))

ts_end = []

for index, t_mix in tqdm(enumerate(ts_mix)):

    #color = colors(index)

    c = solve(
        W=W, 
        H=H, 
        dx=dx, 
        dy=dy, 
        D=D, 
        c1_init=c1_init, 
        c2_init=c2_init, 
        threshold=0.02, 
        t_mix=t_mix, 
        debug=True)
    
    check_solution(c)

    T = c.shape[1]
    # skip as many frames as needed
    # to keep file sizes small and 
    # frame count around 200
    stride = max(1, int(T / 200))
    c1, c2, c3 = c[:, ::stride, :, :]

    ts = np.linspace(0, T * dt, c1.shape[0])

    mix_frame = int(len(ts) * t_mix / unmixed_stop_time)
    
    q = np.sum(c3, axis=(1, 2))
    plt.plot(ts, q, label=f'$t_{{mix}}={int(t_mix)}$')
    plt.scatter(ts[-1], q[-1])

    ts_end.append(T * dt)

    plt.vlines(x=t_mix, ymin=0, ymax=0.1, ls='--')

ts_end = np.array(ts_end)

title = f'Medžiagos $c_3$ kiekio $q_3(t)=\\sum_{{i=0}}^{{N-1}}\\sum_{{j=0}}^{{M-1}}c_3(i, j, t)$ priklausomybė nuo laiko.'
plt.title(title)
plt.xlabel('$t$')
plt.ylabel('$q_3$')
plt.show()

array = np.column_stack((ts_mix, ts_end))
np.save('saves/mix-times_other.npy', array)

# %%
