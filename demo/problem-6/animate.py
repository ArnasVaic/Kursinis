# %%

from pathlib import Path
from typing import Callable
import configparser
import numpy as np
from tqdm import tqdm
import numpy.typing as npt
import matplotlib.pyplot as plt
import matplotlib.animation as plta
from simid import simulation_identifier 

plt.rcParams['animation.ffmpeg_path'] = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'

config = configparser.ConfigParser() 
config.read('simulation-parameters.ini')
params = config['DEFAULT']

filename = simulation_identifier(params, 'npy')
c = np.load(f'saves/optimized/{filename}')
print(f'Loaded configuration: {simulation_identifier(params)}')

L = float(params['L'])
T = int(params['T'])
DX = float(params['DX'])
DY = float(params['DY'])
D = float(params['D'])
K1 = float(params['K1'])
K2 = float(params['K2'])
K3 = float(params['K3'])
SIZE_X, SIZE_Y = c.shape[1], c.shape[2]

c1, c2, c3 = c[0], c[1], c[2]

DT1 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 3 * np.max(c2[:, :, 0]))
DT2 = 1 / (2 * D * (1/DX**2 + 1/DY**2) + 5 * np.max(c1[:, :, 0]))
DT = np.min([DT1, DT2]) 

frame_stride = int(params['FrameStride'])

def animate_parametrized(frame: int, f: npt.NDArray[np.float64], c_index: int):
  t = frame * frame_stride
  plt.clf()
  plt.xlabel('$x$')
  plt.ylabel('$y$')
  plt.title(f'$c_{c_index}(x,y,t)$ at time $t={DT * (t + frame_stride):.02f}$\n{simulation_identifier(params)}')
  plt.imshow(f[:, :, t].T, cmap='inferno', extent=(0, L, 0, L), vmin=0, vmax=1)
  plt.colorbar()

FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])

video_dir = simulation_identifier(params)
video_path = Path(f'videos/optimized/{video_dir}')
if not video_path.exists():
  video_path.mkdir(parents=True, exist_ok=True)

for i, c in tqdm(enumerate([c1, c2, c3])):
  #print(f'Animating c{i + 1}')
  animate_func: Callable[[int], None] = lambda frame: animate_parametrized(frame, c, i+1)
  animation = plta.FuncAnimation(plt.gcf(), animate_func, frames=int(T/frame_stride), interval=20)
  FFwriter = plta.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])

  filename = Path(f'c{i + 1}.mp4')
  animation.save(video_path / filename, writer=FFwriter)

# %%
