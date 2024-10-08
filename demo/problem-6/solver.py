import numpy as np
from scipy.signal import convolve2d
from mixer import mix

def get_dt(dx, dy, D, c1_max, c2_max):
  return 1 / (2 * D * (dx ** -2 + dy ** -2) - min(3 * c2_max, 5 * c1_max))

def solve(W, H, dx, dy, D, c1_init, c2_init, t_mix=None, debug=False):

  laplacian_filter = np.array([
    [        0,                  dy ** -2 ,        0 ],
    [ dx ** -2, -2 * (dx ** -2 + dy ** -2), dx ** -2 ],
    [        0,                  dy ** -2 ,        0 ]
  ])

  def laplacian(c):
    padded = np.pad(c, (1, 1), 'edge')
    return convolve2d(padded, laplacian_filter, mode='valid')

  dt = get_dt(dx, dy, D, c1_init.max(), c2_init.max())

  width, height = int(W / dx) + 1, int(H / dy) + 1
  c1, c2, c3 = [ c1_init ], [ c2_init ], [ np.zeros((width, height)) ]
 
  # stop reaction when ratio of elements c1, c2 
  # to the initial amount reaches threshold 
  threshold = 0.30
  c1c2_qnt0 = (c1_init[:, :] + c2_init[:, :]).sum()

  t = 0

  while True:

    if t_mix is not None and abs(t * dt - t_mix) <= dt / 2:
      c1[t], c2[t], c3[t] = mix([c1[t], c2[t], c3[t]])

    c1c2 = c1[t][:, :] * c2[t][:, :]
    c1.append(c1[t][:, :] - 3 * dt * c1c2 + dt * D * laplacian(c1[t][:, :]))
    c2.append(c2[t][:, :] - 5 * dt * c1c2 + dt * D * laplacian(c2[t][:, :]))
    c3.append(c3[t][:, :] + 2 * dt * c1c2)

    c1c2_qnt = (c1[t + 1][:, :] + c2[t + 1][:, :]).sum()

    if debug:
      if t % 1000 == 0:
        print(f'q = {c1c2_qnt / c1c2_qnt0}')

    if c1c2_qnt / c1c2_qnt0 <= threshold:
      break

    t = t + 1
  
  c1 = np.stack(c1, axis=0)
  c2 = np.stack(c2, axis=0)
  c3 = np.stack(c3, axis=0)

  # shape [ 3, t, width, height ]
  return np.stack((c1, c2, c3), axis=0)