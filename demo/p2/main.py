# %%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as plta

# problems:
# slow animation rendering
# detail has impact on animation speed

DX = DY = 0.01 # spatial step
N = (100, 100) # sheet resolution
T = 400 # number of time steps to simulate
K = 1 # thermal diffusivity

# boundary condition (constant corner temperature)
# top left, top right, bottom left, bottom right
U0 = (0, 50, 50, 100) 

# choose such time step that numerical stability is ensured
DT = (DX ** 2) * (DY ** 2) / (2 * K * (DX**2 + DY**2))

# array that will store information about the 
# sheet temperature at all time steps until step T
u = np.zeros([*N, T])

# boundary conditions
u[0, 0, :] = U0[0]
u[0, -1, :] = U0[1]
u[-1, 0, :] = U0[2]
u[-1, -1, :] = U0[3]

for t in range(T - 1):
  for x in range(N[0]):
    for y in range(N[1]):
      
      d2ux = 0 if x == 0 or x == N[0] - 1 else (u[x + 1, y, t] - 2 * u[x, y, t] + u[x - 1, y, t]) / (DX ** 2) 
      d2uy = 0 if y == 0 or y == N[1] - 1 else (u[x, y + 1, t] - 2 * u[x, y, t] + u[x, y - 1, t]) / (DY ** 2)
      
      u[x, y, t + 1] = u[x, y, t] + K * DT * (d2ux + d2uy)

# render animation
def render(frame):
  plt.clf()  
  plt.imshow(u[:, :, frame].T, extent=[0, 1, 0, 1], cmap='hot')
  plt.colorbar()
  plt.title(f'Frame {1 + frame}/{T}')

animation = plta.FuncAnimation(plt.gcf(), render, frames=T, interval=20)
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'
FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
animation.save('sheet.mp4', writer=FFwriter)
# %%
