# %%

from typing import Callable
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import matplotlib.animation as plta

plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'

LOAD_DIR = 'saves/optimized'
FILENAME = '[n,t,cs]=[100,10000,0]-optimized'
c = np.load(f'{LOAD_DIR}/{FILENAME}.npy')

print(c.shape)

SIZE_X, SIZE_Y = c.shape[1], c.shape[2]
DX, DY, T = 1 / SIZE_X, 1 / SIZE_Y, c.shape[3],
D = 1/4 # Diffusivity constant

c1, c2, c3 = c[0], c[1], c[2]

print(f'T={T}, SIZE=({SIZE_X}, {SIZE_Y})')
print(c1.shape, c2.shape, c3.shape)

DT1 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 3 * np.max(c2[:, :, 0]))
DT2 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 5 * np.max(c1[:, :, 0]))
DT = np.min([DT1, DT2]) 

frame_stride = 50 # only render every 50 frames for long simulations

def animate_parametrized(frame: int, c: npt.NDArray[np.float64], c_index: int):
  t = frame * frame_stride
  plt.clf()
  plt.xlabel('x')
  plt.ylabel('y')
  plt.title(f'Values of c_{c_index}(x, y, t) at time t={DT * (t + frame_stride):.02f}')
  plt.imshow(c[:, :, t].T, cmap='inferno', extent=[0, 1, 0, 1], vmin=0, vmax=1)
  plt.colorbar()

FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])

for i, c in enumerate([c1, c2, c3]):
  animate_func: Callable[[int], None] = lambda frame: animate_parametrized(frame, c, i+1)
  animation = plta.FuncAnimation(plt.gcf(), animate_func, frames=int(T/frame_stride), interval=20)
  FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
  animation.save(f'videos/optimized/c{i+1}-{FILENAME}.mp4', writer=FFwriter)

# %%
