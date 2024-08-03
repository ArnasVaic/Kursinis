# %%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as plta

# problems:
# slow animation rendering
# detail has impact on animation speed

DX = 0.01 # spatial step
N = 24 # size of rod (has influence to the speed to heat propagation)
T = 400 # number of time steps to simulate
K = 1 # thermal diffusivity
T1 = 50 # temperature at the left end of the rod
T2 = 100 # temperature at the right end of the rod

# choose such time step that numerical stability is ensured
DT = (DX ** 2) / (2 * K)

# array that will store information about the 
# rod temperature at all time steps until step T
u = np.zeros([N, T])

# set boundary conditions
u[0, :], u[-1, :] = T1, T2

for t in range(T - 1):
  # iterate through cells but skip first and last ones
  # because their temperature will always remain the same
  for x in range(1, N - 1):
    # in larger dimensions this would be the laplacian but in 1D 
    # this is just the second derivative of u with respect to x
    laplacian = (u[x + 1, t] - 2 * u[x, t] + u[x - 1, t]) / (DX ** 2)
    
    # formula derived in README.md
    # technically we always choose dt such that coef next to u(x, t) 
    # would be 0 so it would be possible to do less operations
    u[x, t + 1] = u[x, t] + K * DT * laplacian

xs = np.arange(0, 1, 1/N)
# render animation
def render(frame):
  plt.clf()  
  plt.plot(xs, u[:, frame])
  ax = plt.gca()
  ax.set_ylim([-0.05 * max(T1, T2), 1.05 * max(T1, T2)])
  plt.title(f'Frame {1 + frame}/{T}')

animation = plta.FuncAnimation(plt.gcf(), render, frames=T, interval=20)
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'
FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
animation.save('rod.mp4', writer=FFwriter)
# %%
