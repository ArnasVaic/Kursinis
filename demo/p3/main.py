# %%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as plta

# problems:
# slow animation rendering
# detail has impact on animation speed

DX = DY = 0.1 # spatial step
N = (24, 24) # sheet resolution
T = 100 # number of time steps to simulate
D = np.array([ 1, 1, 1 ]) # thermal diffusivity for different materials
K = np.array([ -3, -5, 8 ]) # reaction rates?
M = 3 # number of channels
# initial amounts of every element uniformly throughout the sheet
C = np.array([ 0.75, 0.5, 0 ])

# choose such time step that numerical stability is ensured
DT = (DX ** 2) * (DY ** 2) / (2 * np.max(D) * (DX**2 + DY**2))

# array that will store information about
# all materials at all time steps until step T
c = np.zeros([M, *N, T])

# initial conditions
c[0, :, :, 0] = C[0]
c[1, :, :, 0] = C[1]
c[2, :, :, 0] = C[2]

for t in range(T - 1):
  for x in range(N[0]):
    for y in range(N[1]):
      d2cx = 0 if x == 0 or x == N[0] - 1 else (c[:, x + 1, y, t] - 2 * c[:, x, y, t] + c[:,x - 1, y, t]) / (DX ** 2)
      d2cy = 0 if y == 0 or y == N[1] - 1 else (c[:, x, y + 1, t] - 2 * c[:, x, y, t] + c[:, x, y - 1, t]) / (DY ** 2)
      lap = d2cx + d2cy      
      c[:, x, y, t + 1] = c[:, x, y, t] + DT * (D * lap + K * c[0, x, y, t]  * c[1, x, y, t] )
      # if x == 10 and y == 10:
      #   print(DT * (D * lap + K * c[0, x, y, t]  * c[1, x, y, t] ))

# %%

element_id = 2

def animate(frame):
  plt.clf()
  plt.xlabel('x')
  plt.ylabel('y')
  plt.title(f'c_{1 + element_id} at {1 + frame}/{T}')
  plt.imshow(c[element_id, :, :, frame], cmap='viridis', vmin=0, vmax=1)
  plt.colorbar()

animation = plta.FuncAnimation(plt.gcf(), animate, frames=T, interval=20)
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'
FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
animation.save('elements.mp4', writer=FFwriter)
plt.show()
# %%
