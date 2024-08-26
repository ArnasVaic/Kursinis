# %%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as plta

DX = DY = 0.01 # spatial step
N = (24, 24) # sheet resolution
T = 400 # number of time steps to simulate
K = 1 # thermal diffusivity

# boundary condition (constant edge temperature)
# top, left, right, bottom
U0 = (0, 50, 50, 100)

# choose such time step that numerical stability is ensured
DT = (DX ** 2) * (DY ** 2) / (2 * K * (DX**2 + DY**2))

# array that will store information about the 
# sheet temperature at all time steps until step T
u = np.zeros([*N, T])

# boundary conditions
u[:,0,:] = U0[0]
u[0,:,:] = U0[1]
u[-1,:,:] = U0[2]
u[:,-1,:] = U0[3]

for t in range(T - 1):
  
  # only update cells that are not on the boundary
  for x in range(1, N[0] - 1):
    for y in range(1, N[1] - 1):
      d2ux = (u[x + 1, y, t] - 2 * u[x, y, t] + u[x - 1, y, t]) / (DX ** 2) 
      d2uy = (u[x, y + 1, t] - 2 * u[x, y, t] + u[x, y - 1, t]) / (DY ** 2)
      u[x, y, t + 1] = u[x, y, t] + K * DT * (d2ux + d2uy)

# render animation
def render(frame):
  plt.clf()  
  plt.imshow(u[:, :, frame].T, extent=[0, 1, 0, 1], cmap='hot')
  plt.colorbar()
  plt.title(f'Frame {1 + frame}/{T}')
  plt.xlabel('x')
  plt.ylabel('y')

animation = plta.FuncAnimation(plt.gcf(), render, frames=T, interval=20)
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'
FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
animation.save('sheet.mp4', writer=FFwriter)
# %%
