# %%

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

# %%
# Simulation configurations
L, T = 1, 10000
DX, DY = 0.01, 0.01
# Thermal diffusivity α (alpha)
A = 1 
DT = (DX**2 * DY**2) / (2 * A * (DX**2 + DY**2))

# Discretized plate size
SIZE_X, SIZE_Y = int(L / DX), int(L / DY)

# %%
# u(x, y, t), (x, y, t) ∈ [0, L] x [0, L] x [0, T]
u = np.zeros([SIZE_X, SIZE_Y, T])

# Initial conditions at t = 0:
# Right edge temperature 100 units and 0 units elsewhere
u[0, :, 0] = 100

def laplacian(
  u: npt.NDArray[np.float64], 
  x: int, 
  y: int, 
  t: int):
  # When x,y is on the boundary some
  # of the neighbours will not exist
  # and will need to be choosen specifically
  # to ensure boundary conditions. In 
  # this case we want to make it so du\dn=0, 
  # where n is the normal along the boundary, 
  # but only for left and top edges, if one 
  # of the neighbours goes out of bounds, we 
  # set its value to be the same as the 
  # current cell u[x, y, t]. As for values 
  # beyond the right and bottom edges, we
  # set them to match initial conditions

  u_center = u[x, y, t]

  # u_{i-1,j}^n
  # left edge always stays at 100
  u_left = 100 if x == 0 else u[x - 1, y, t]

  # u_{i+1,j}^n
  # right edge has du\dx = 0, so value 
  # "beyond" border should match u_center
  u_right = u_center if x == SIZE_X - 1 else u[x + 1, y, t]

  # u_{i,j+1}^n
  # top edge has du\dy = 0, so value 
  # "beyond" border should match u_center
  u_top = u_center if y == 0 else u[x, y - 1, t]

  # u_{i,j-1}^n
  # bottom edge always stays at 0
  u_bottom = 0 if y == SIZE_Y - 1 else u[x, y + 1, t]

  # laplacian components of each dimension (to keep line length small)
  lap_x = (u_left - 2 * u_center + u_right) / (DX**2)
  lap_y = (u_top - 2 * u_center + u_bottom) / (DY**2)

  return lap_x + lap_y

for t in range(T - 1):
  for x in range(SIZE_X):
    for y in range(SIZE_Y): 
      u[x, y, t + 1] = u[x, y, t] + A * DT * laplacian(u, x, y, t)
# %%

t_view = 9999
plt.xlabel('x')
plt.ylabel('y')
display_time = DT * (999 + 1)
plt.title(f'Values of u(x, y, t) at time t={display_time:.02f}')
plt.imshow(u[:, :, t_view].T, cmap='inferno', extent=[0, L, 0, L])

# %%
np.save('u_100x100_t10000.npy', u)

# %%

import matplotlib.animation as plta

u = np.load('u_100x100_t10000.npy')
frame_stride = 50 # only render every 50 frames

def animate(frame: int):
  t = frame * frame_stride
  plt.clf()
  plt.xlabel('x')
  plt.ylabel('y')
  plt.title(f'Values of u(x, y, t) at time t={DT * (t + frame_stride):.02f}')
  plt.imshow(u[:, :, t].T, cmap='inferno', extent=[0, L, 0, L], vmin=np.min(u[:,:,0]), vmax=np.max(u[:,:,0]))
  plt.colorbar()

animation = plta.FuncAnimation(plt.gcf(), animate, frames=int(T/frame_stride), interval=20)
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'
FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
animation.save('video.mp4', writer=FFwriter)
# %%
