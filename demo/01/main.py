# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def show(frame):
  plt.imshow(frame.T, cmap='plasma')
  plt.colorbar()
  plt.show()

def set_boundary_zero(inp):
  inp[0, :] = inp[-1, :] = inp[:, 0] = inp[:, -1] = 0
  return inp

dx = dy = 0.02
W, H, T = 1, 1, 100
u = np.zeros([T, int(W / dx), int(H / dy)])

# thermal diffusivity
k = 6
# largest possible time step that ensures numerical stability
dt = (dx ** 2 * dy ** 2) / (2 * k * (dx ** 2 + dy ** 2))

# initial configuration (checker pattern 2x2)
# u[0, :int(W / dx)//2, :int(H / dy)//2] = 100
# u[0, int(W / dx)//2:, int(H / dy)//2:] = 100

# First internet example (100C rod at the top boundary)
# u[0,1:-1,0] = 100

# Second internet example (random noise)
u[0, :, :] = np.random.uniform(low=28.5, high=55.5, size=(int(W/dx), int(H/dy)))
u[0] = set_boundary_zero(u[0])

show(u[0])

# Kernel used to calculate finite differences
kernel = np.array([
  [0, 1 / (dy**2), 0],
  [1 / (dx**2), -2 * ( 1 / (dx**2) + 1 / (dy**2) ), 1 / (dx**2)],
  [0, 1 / (dy**2), 0]
])

def update(u):
  laplacian = convolve2d(u, kernel, mode='same', fillvalue=0)
  laplacian = set_boundary_zero(laplacian)
  return u + k * dt * laplacian

for t in range(T - 1):
  u[t + 1] = update(u[t])

def update_frame(frame):
  plt.clf()
  plt.imshow(u[frame].T, cmap='viridis')
  plt.title(f'Time Step {dt * frame:.2f}')
  plt.colorbar()

animation = FuncAnimation(plt.gcf(), update_frame, frames=T, interval=20)

animation.save('noise.gif')
# %%
