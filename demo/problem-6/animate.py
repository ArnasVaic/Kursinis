# %%

from pathlib import Path
from typing import Callable
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import matplotlib.animation as plta
from solver_config import *
from solver import *

plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'

id = solver_config_id()
c1, c2, c3 = np.load(f'saves/{id}.npy')
print(f'Loaded configuration: {id}')

W, H = solver_config['W'], solver_config['H']
dx, dy = solver_config['dx'], solver_config['dy']
D = solver_config['D']

dt = get_dt(dx, dy, D, c1[0].max(), c2[0].max())

print(f'dt = {dt}')

T, N, M = c3.shape

FRAME_STRIDE = 1

c_max = [ c1.max(), c2.max(), c3.max() ]

def animate_parametrized(frame: int, f: npt.NDArray[np.float64], c_index: int):
  t = frame * FRAME_STRIDE
  plt.clf()
  plt.xlabel('$x$')
  plt.ylabel('$y$')
  plt.title(f'$c_{c_index}(x,y,t)$ at time $t={dt * t * 25:.02f}$\n{id}')
  #plt.imshow(f[t, :, :].T, cmap='inferno', extent=(0, W, H, 0), vmin=0, vmax=c_max[c_index - 1], origin="upper")
  plt.imshow(f[t, :, :].T, cmap='inferno', extent=(0, W, H, 0), origin="upper")
  plt.colorbar()

FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])

video_path = Path(f'videos/{id}')
if not video_path.exists():
  video_path.mkdir(parents=True, exist_ok=True)

for i, c in enumerate([c1, c2, c3]):
  animate_func: Callable[[int], None] = lambda frame: animate_parametrized(frame, c, i+1)
  animation = plta.FuncAnimation(plt.gcf(), animate_func, frames=int(T/FRAME_STRIDE), interval=20)
  FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])

  filename = Path(f'c{i + 1}.mp4')
  animation.save(video_path / filename, writer=FFwriter)

# %%
