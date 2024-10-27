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
 
  c1, c2, c3 = c

  # if c1.min() < 0:
  #   id = np.unravel_index(c1.argmin(), c1.shape)
  #   print(f'c1 min: {c1.min()} at {id}')

  # if c2.min() < 0:
  #   id = np.unravel_index(c2.argmin(), c2.shape)
  #   print(f'c2 min: {c2.min()} at {id}')

  # if c3.min() < 0:
  #   id = np.unravel_index(c3.argmin(), c3.shape)
  #   print(f'c3 min: {c3.min()} at {id}')

  # material quantities over time
  q1 = np.sum(c1, axis=(1, 2))
  q2 = np.sum(c2, axis=(1, 2))
  q3 = np.sum(c3, axis=(1, 2))

  # rates of change of material quantities through time
  q1dt = np.diff(q1, 1, axis=0)
  q2dt = np.diff(q2, 1, axis=0)
  q3dt = np.diff(q3, 1, axis=0)

  # if np.any(q1dt >= sys.float_info.epsilon):
  #   id = np.unravel_index(q1dt.argmax(), q1dt.shape)
  #   print(f'q1dt[{id[0]}]={q1dt[id]}')

  # if np.any(q2dt >= sys.float_info.epsilon):
  #   id = np.unravel_index(q2dt.argmax(), q2dt.shape)
  #   print(f'q2dt[{id[0]}]={q2dt[id]}')

  # if np.any(q3dt < sys.float_info.epsilon):
  #   id = np.unravel_index(q3dt.argmin(), q3dt.shape)
  #   print(f'q3dt[{id[0]}]={q3dt[id]}')

  # assert 1st & 2nd materials quantities are always non-negative and non-increasing
  assert np.all(c1 >= 0)
  assert np.all(q1dt <= 0)

  assert np.all(c2 >= 0)
  assert np.all(q2dt <= 0)

  # assert 3rd material quantity is non-negative and non-decreasing
  assert np.all(c3 >= 0)
  assert np.all(q3dt >= 0)

def stop(t, T, c1, c2, threshold):
  relative_quantity = (c1[t] + c2[t]).sum() / (c1[0] + c2[0]).sum()
  return (T is None and relative_quantity <= threshold)  \
      or (T is not None and t == T)

def build_laplacian_filter(dx, dy):
  return np.array([
    [      0,            dy**-2 ,      0 ],
    [ dx**-2, -2*(dx**-2+dy**-2), dx**-2 ],
    [      0,            dy**-2 ,      0 ]
  ])

def laplacian(c, filter):
  padded = np.pad(c, (1, 1), 'edge')
  return convolve2d(padded, filter, mode='valid')

def validate_inputs(
  W, 
  H, 
  N, 
  M,
  D, 
  c1_init, 
  c2_init, 
  threshold, 
  t_mix,
  T,
  dt):
  assert W > 0
  assert H > 0

  assert N > 0
  assert type(N) is int
  
  assert M > 0
  assert type(M) is int

  assert D >= 0

  assert np.all(c1_init >= 0)
  assert np.all(c2_init >= 0)

  assert threshold is None or 0 <= threshold <= 1

  assert t_mix is None or t_mix >= 0

  assert type(T) is int
  assert T is None or T > 0

  assert (threshold and t_mix) or T

  dx = W / (N - 1)
  dy = H / (M - 1)

  dt_upper_bound = get_upper_dt_bound(dx, dy, D, c1_init, c2_init)
  if dt is not None and dt_upper_bound < dt:
    print(f'warning: it must hold that dt <= {dt_upper_bound}')
  assert dt is None or dt_upper_bound >= dt

def print_initial_debug_info(T, dt, dt_upper_bound, t_mix, threshold):

  if T is None:
    print(f'Will stop when quantity of initial elements reaches threshold ({threshold}).')
  else:
    print(f'Will stop at time step T={T}.')

  print(f'Upper dt bound: {dt_upper_bound}, given dt={dt}')

  if t_mix is not None:
    print(f"approximate frame of mixing: {int(t_mix / dt)}")

def print_sim_debug_info(t, dt, c1, c2):
  q1 = c1[t].sum() / c1[0].sum()
  q2 = c2[t].sum() / c2[0].sum()
  q = (c1[t] + c2[t]).sum() / (c1[0] + c2[0]).sum()
  print(f'[t={t * dt:.02f},step={t}] [q1 q2 q]=[{q1:.02f} {q2:.02f} {q:.02f}]')

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

  validate_inputs(W, H, N, M, D, c1_init, c2_init, threshold, t_mix, T, dt)

  dx = W / (N - 1)
  dy = H / (M - 1)
  dt_upper_bound = get_upper_dt_bound(dx, dy, D, c1_init.max(), c2_init.max())

  if debug:
    print_initial_debug_info(T, dt, dt_upper_bound, t_mix, threshold)
  
  filter = build_laplacian_filter(dx, dy)
  dt = dt or dt_upper_bound
  c1, c2, c3 = [ c1_init ], [ c2_init ], [ np.zeros((N, M)) ]
  t = 0
  mixing_done = False

  while True:

    if debug and t % 2000 == 0:
      print_sim_debug_info(t, dt, c1, c2)

    if t_mix is not None and abs(t * dt - t_mix) <= dt / 2 and not mixing_done:
      if debug:
        print(f'[t={t * dt:.02f},step={t}] mixing')
      c1[t], c2[t], c3[t] = mix([c1[t], c2[t], c3[t]], B=B, debug=False)

    c1_next = c1[t] + dt * (-3 * c1[t] * c2[t] + D * laplacian(c1[t], filter))
    c2_next = c2[t] + dt * (-5 * c1[t] * c2[t] + D * laplacian(c2[t], filter))
    c3_next = c3[t] + dt *   2 * c1[t] * c2[t]

    _ = c1.append(c1_next), c2.append(c2_next), c3.append(c3_next)

    # if T is not set, stop reaction when ratio of elements c1, c2 
    # to the initial amount reaches threshold 
    if stop(t, T, c1, c2, threshold):
      break

    # update time step
    t = t + 1

  # convert python lists to numpy lists
  c1 = np.stack(c1, axis=0)
  c2 = np.stack(c2, axis=0)
  c3 = np.stack(c3, axis=0)

  # shape [ 3, t, width, height ]
  c = np.stack((c1, c2, c3), axis=0)
  validate_solution(c)
  
  return c 