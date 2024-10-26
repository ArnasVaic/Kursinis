import numpy as np
from scipy.signal import convolve2d
from mixer import mix
import sys

def get_upper_dt_bound(dx, dy, D, c1_initial, c2_initial):
  
  c1_initial_max = c1_initial.max()
  c2_initial_max = c2_initial.max() 

  return 1 / np.max([
    2 * D * (dx**-2 + dy**-2) + 3 * c2_initial_max,
    2 * D * (dx**-2 + dy**-2) + 5 * c1_initial_max
  ])

def validate_dt(dt, dx, dy, D, c1_initial, c2_initial):
  dt_upper_bound = get_upper_dt_bound(dx, dy, D, c1_initial, c2_initial)

  if dt_upper_bound < dt:
    print(f'error: given dt={dt:.04f} may produce unstable results! Use dt <= {dt_upper_bound:04f}.')
  assert dt_upper_bound >= dt

def validate_solution(c):
  """Validate solution

  Args:
      c (_type_): _description_
  """
  c1, c2, c3 = c

  # material quantities over time
  q1 = np.sum(c1, axis=(1, 2))
  q2 = np.sum(c2, axis=(1, 2))
  q3 = np.sum(c3, axis=(1, 2))

  # rates of change of material quantities through time
  q1dt = np.diff(q1, 1, axis=0)
  q2dt = np.diff(q2, 1, axis=0)
  q3dt = np.diff(q3, 1, axis=0)

  if c1.min() < 0:
    id = np.unravel_index(c1.argmin(), c1.shape)
    print(f'c1 min: {c1.min()} at {id}')

  if c2.min() < 0:
    id = np.unravel_index(c2.argmin(), c2.shape)
    print(f'c2 min: {c2.min()} at {id}')

  if c3.min() < 0:
    id = np.unravel_index(c3.argmin(), c3.shape)
    print(f'c3 min: {c3.min()} at {id}')

  if np.any(q1dt >= sys.float_info.epsilon):
    id = np.unravel_index(q1dt.argmax(), q1dt.shape)
    print(f'q1dt[{id[0]}]={q1dt[id]}')

  if np.any(q2dt >= sys.float_info.epsilon):
    id = np.unravel_index(q2dt.argmax(), q2dt.shape)
    print(f'q2dt[{id[0]}]={q2dt[id]}')

  if np.any(q3dt < sys.float_info.epsilon):
    id = np.unravel_index(q3dt.argmin(), q3dt.shape)
    print(f'q3dt[{id[0]}]={q3dt[id]}')

  # assert 1st & 2nd materials quantities are always non-negative and non-increasing
  assert 0 <= c1.min() <= sys.float_info.epsilon
  #assert np.all(q1dt <= sys.float_info.epsilon)

  assert 0 <= c2.min() <= sys.float_info.epsilon
  #assert np.all(q2dt <= sys.float_info.epsilon)

  # assert 3rd material quantity is non-negative and non-decreasing
  assert 0 <= c3.min() <= sys.float_info.epsilon
  assert np.all(q3dt >= 0)

def solve(
  W, 
  H, 
  N, 
  M,
  D, 
  c1_init, 
  c2_init, 
  threshold=None, 
  t_mix=None, 
  B=2,
  debug=False,
  T=None,
  dt=None):

  assert threshold or T

  dx = W / (N - 1)
  dy = H / (M - 1)

  # setup laplacian methods
  laplacian_filter = np.array([
    [      0,            dy**-2 ,      0 ],
    [ dx**-2, -2*(dx**-2+dy**-2), dx**-2 ],
    [      0,            dy**-2 ,      0 ]
  ])

  def laplacian(c):
    padded = np.pad(c, (1, 1), 'edge')
    return convolve2d(padded, laplacian_filter, mode='valid')

  # validate/choose dt
  dt_upper_bound = get_upper_dt_bound(dx, dy, D, c1_init.max(), c2_init.max())

  if dt is not None:
    validate_dt(dt, dx, dy, D, c1_init, c2_init)
  
  dt = dt or dt_upper_bound

  c1, c2, c3 = [ c1_init ], [ c2_init ], [ np.zeros((N, M)) ]

  if debug:
    if T is None:
      print(f'Stopping when quantity of initial elements reaches threshold.')
    else:
      print(f'Stopping on time step T={T}.')
    print(f'upper dt bound: {dt_upper_bound}, given dt={dt}')

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

    c1_curr = c1[t][:, :]
    c2_curr = c2[t][:, :]
    c3_curr = c3[t][:, :]

    c1c2 = c1_curr * c2_curr

    c1_next = c1_curr + dt * (-3 * c1c2 + D * laplacian(c1_curr))
    c2_next = c2_curr + dt * (-5 * c1c2 + D * laplacian(c2_curr))
    c3_next = c3_curr + dt * 2 * c1c2

    print(c2_next)

    c1.append(c1_next)
    c2.append(c2_next)
    c3.append(c3_next)

    c1c2_qnt = (c1_next + c2_next).sum()

    if debug:
      if t % 2000 == 0:
        q1 = c1_next.sum() / c1_init.sum()
        q2 = c2_next.sum() / c2_init.sum()
        q = c1c2_qnt / c1c2_qnt0
        print(f'[t={t * dt:.02f}][q1 q2 q]=[{q1:.02f} {q2:.02f} {q:.02f}]')

    # if T is not set, stop reaction when ratio of elements c1, c2 
    # to the initial amount reaches threshold 
    if T is None and c1c2_qnt / c1c2_qnt0 <= threshold:
      break

    # if T is set, stop reaction when last time step is reached
    if T is not None and t == T:
      break

    # update time step
    t = t + 1

  # convert python lists to numpy lists
  c1 = np.stack(c1, axis=0)
  c2 = np.stack(c2, axis=0)
  c3 = np.stack(c3, axis=0)

  # shape [ 3, t, width, height ]
  return np.stack((c1, c2, c3), axis=0)