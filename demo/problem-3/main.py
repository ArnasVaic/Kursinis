# %%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as plta

DX = DY = 1 # spatial step
N = np.array([24, 24]) # sheet resolution
T = 400 # number of time steps to simulate
D = np.array([ 1, 1, 1 ]) # thermal diffusivity for different materials
K = np.array([ -3, -5, 2 ]) # reaction rates?
M = 3 # number of channels

# choose such time step that numerical stability is ensured
# this formula assumes C_i <= 1
DT = 1 / (2 * np.max(D) * (DX**-2 + DY**-2) - np.min(K))

# array that will store information about
# all materials at all time steps until step T
c = np.zeros([M, *N, T])

# initial conditions (overlapping squares)
sixth = 2 * N // 24
half = 20 * N // 24

# element 0
# tl0 = sixth # top left
# br0 = tl0 + half - [1, 1] # bottom right
# # element 1
# tl1 = 2 * sixth
# br1 = tl1 + half - [1, 1]

# c[0, tl0[0]:br0[0], tl0[1]:br0[1], 0] = 1
# c[1, tl1[0]:br1[0], tl1[1]:br1[1], 0] = 1

# initial conditions (constant uniform amount)
# c[0, :, :, 0] = c[1, :, :, 0] = 1

# initial conditions (overlapping rectangles, symmetric along y)
c[0, :7 * N[0] // 12 , :, 0] = 1
c[1,  5 * N[0] // 12:, :, 0] = 1

for t in range(T - 1):
  for x in range(N[0]):
    for y in range(N[1]):
      ci_t = c[:, x, y ,t]
      # if we're on the boundary of x/y set the laplacian x/y 
      # component to 0 in my mind this should enforce that no 
      # material is lost through the border, but i'm not 100% sure.
      d2cx = 0 if x == 0 or x == N[0] - 1 else (c[:, x + 1, y, t] - 2 * ci_t + c[:,x - 1, y, t]) / (DX ** 2)
      d2cy = 0 if y == 0 or y == N[1] - 1 else (c[:, x, y + 1, t] - 2 * ci_t + c[:, x, y - 1, t]) / (DY ** 2)
      lap = d2cx + d2cy
      c[:, x, y, t + 1] = ci_t + DT * (D * lap + K * ci_t[0] * ci_t[1])

# %%

def animate(frame):
  plt.clf()
  plt.xlabel('x')
  plt.ylabel('y')
  plt.title(f'c at {1 + frame}/{T}')
  plt.imshow(np.transpose(c[:, :, :, frame], (2, 1, 0)), extent=[0,1,0,1])

animation = plta.FuncAnimation(plt.gcf(), animate, frames=T, interval=20)
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'
FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
animation.save('elements.mp4', writer=FFwriter)


# %%
