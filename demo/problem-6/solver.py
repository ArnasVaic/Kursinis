import numpy as np
from scipy.signal import convolve2d
from mixer import mix
import sys

def get_dt(dx, dy, D, c1_max, c2_max):

  D_x = D / dx
  D_y = D / dy

  return 1 / np.max([
    2 * (D_x/dx**2 + D_y/dy**2) + 3 * c2_max,
    2 * (D_x/dx**2 + D_y/dy**2) + 5 * c1_max
  ])

def check_solution(c):
  c1, c2, c3 = c

  # material quantities over time
  q1 = np.sum(c1, axis=(1, 2))
  q2 = np.sum(c2, axis=(1, 2))
  q3 = np.sum(c3, axis=(1, 2))

  # rates of change of material quantities through time
  q1dt = np.diff(q1, 1, axis=0)
  q2dt = np.diff(q2, 1, axis=0)
  q3dt = np.diff(q3, 1, axis=0)

  # assert 1st & 2nd materials quantities are always non-negative and non-increasing
  assert 0 <= c1.min() <= sys.float_info.epsilon
  assert np.all(q1dt <= 0)

  assert 0 <= c2.min() <= sys.float_info.epsilon
  assert np.all(q2dt <= 0)

  # assert 3rd material quantity is non-negative and non-decreasing
  assert 0 <= c3.min() <= sys.float_info.epsilon
  assert np.all(q3dt >= 0)

def solve(
  W, 
  H, 
  dx, 
  dy,
  D, 
  c1_init, 
  c2_init, 
  threshold, 
  t_mix=None, 
  B=2,
  debug=False,
  T=None,
  dt=None):

  D_x, D_y = D / dx, D / dy

  laplacian_filter = np.array([
    [        0,                  D_y * dy ** -2 ,        0 ],
    [ D_x * dx ** -2, -2 * (D_x * dx ** -2 + D_y * dy ** -2), D_x * dx ** -2 ],
    [        0,                  D_y * dy ** -2 ,        0 ]
  ])

  def laplacian(c):
    padded = np.pad(c, (1, 1), 'edge')
    return convolve2d(padded, laplacian_filter, mode='valid')

  dt_safe = get_dt(dx, dy, D, c1_init.max(), c2_init.max())
  if debug and dt is not None and dt > dt_safe:
    print(f'warning: given dt may produce unstable results!')
    print(f'suggestion: use dt below or equal to {dt_safe:02f}')

  dt = dt or dt_safe

  width, height = round(W / dx) + 1, round(H / dy) + 1
  c1, c2, c3 = [ c1_init ], [ c2_init ], [ np.zeros((width, height)) ]

  if debug:
    if T is None:
      print(f'Stopping when quantity of initial elements reaches threshold.')
    else:
      print(f'Stopping on time step T={T}.')
    print(f'discrete grid size: ({width}, {height})')
    print(f'dt = {dt}')
    print(f'D = ({D_x}, {D_y})')
    if t_mix is not None:
      print(f"approximate frame of mixing: {int(t_mix / dt)}")
  
  c1c2_qnt0 = (c1_init[:, :] + c2_init[:, :]).sum()

  t = 0

  mixing_done = False

  while True:

    if t_mix is not None and abs(t * dt - t_mix) <= dt / 2 and not mixing_done:
      if debug:
        print(f'mixing at t = {t * dt:.02f} (frame: {t})')
      c1[t], c2[t], c3[t] = mix([c1[t], c2[t], c3[t]], B=B, debug=False)

    c1c2 = c1[t][:, :] * c2[t][:, :]
    c1.append(c1[t][:, :] - 3 * dt * c1c2 + dt * laplacian(c1[t][:, :]))
    c2.append(c2[t][:, :] - 5 * dt * c1c2 + dt * laplacian(c2[t][:, :]))
    c3.append(c3[t][:, :] + 2 * dt * c1c2)

    c1c2_qnt = (c1[t + 1][:, :] + c2[t + 1][:, :]).sum()

    if debug:
      if t % 2000 == 0:
        q1 = c1[t + 1][:, :].sum() / c1_init[:, :].sum()
        q2 = c2[t + 1][:, :].sum() / c2_init[:, :].sum()
        q = c1c2_qnt / c1c2_qnt0
        print(f'[t={t * dt:.02f}][q1 q2 q]=[{q1:.02f} {q2:.02f} {q:.02f}]')

    # stop reaction when ratio of elements c1, c2 
    # to the initial amount reaches threshold 
    #
    if T is None and c1c2_qnt / c1c2_qnt0 <= threshold:
      break

    if T is not None and t == T:
      break

    t = t + 1

  # convert python lists to numpy lists
  c1 = np.stack(c1, axis=0)
  c2 = np.stack(c2, axis=0)
  c3 = np.stack(c3, axis=0)

  # shape [ 3, t, width, height ]
  return np.stack((c1, c2, c3), axis=0)