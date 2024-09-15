# %%

from typing import Callable
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import matplotlib.animation as plta

plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'

L, T = 1, 10000
D = 1/4 # Diffusivity constant
DX, DY = 0.01, 0.01
SIZE_X, SIZE_Y = int(L / DX), int(L / DY)

c1 = np.load(f'saves/c1_{SIZE_X}x{SIZE_Y}_t{T}-adjusted-coef.npy')
c2 = np.load(f'saves/c2_{SIZE_X}x{SIZE_Y}_t{T}-adjusted-coef.npy')
c3 = np.load(f'saves/c3_{SIZE_X}x{SIZE_Y}_t{T}-adjusted-coef.npy')

DT1 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 3 * np.max(c2[:, :, 0]))
DT2 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 5 * np.max(c1[:, :, 0]))
DT = np.min([DT1, DT2]) 

frame_stride = 50 # only render every 50 frames

def animate_parametrized(frame: int, c: npt.NDArray[np.float64], c_index: int):
  t = frame * frame_stride
  plt.clf()
  plt.xlabel('x')
  plt.ylabel('y')
  plt.title(f'Values of c_{c_index}(x, y, t) at time t={DT * (t + frame_stride):.02f}')
  plt.imshow(c[:, :, t].T, cmap='inferno', extent=[0, L, 0, L], vmin=0, vmax=1)
  plt.colorbar()

FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])

for i, c in enumerate([c1, c2, c3]):
  animate_func: Callable[[int], None] = lambda frame: animate_parametrized(frame, c, i+1)
  animation = plta.FuncAnimation(plt.gcf(), animate_func, frames=int(T/frame_stride), interval=20)
  FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
  animation.save(f'videos/c{i+1}_{SIZE_X}x{SIZE_Y}_t{T}-adjusted-coef.mp4', writer=FFwriter)

# %%
