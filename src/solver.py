import sys
import numpy as np
from scipy.signal import convolve2d
from initial_config import get_larger_c_init
from mixer import mix

def get_upper_dt_bound_from_config(config):
  W = config['W']
  H = config['H']
  N = config['N']
  M = config['M']
  D  = config['D']
  c0 = config['c0']
  k = config['k']
  dx = W / (N - 1)
  dy = H / (M - 1)
  return get_upper_dt_bound(dx, dy, D, c0, k)

def get_upper_dt_bound(dx: float, dy: float, D: float, c0: float, k: float):
  """Get upper bound for the time step

  Args:
      dx (float): step size in x
      dy (float): step size in y
      D (float): diffusion coefficient
      c0 (float): initial concentration
      k (float): reactivity coefficient

  Returns:
      float: upper bound for time step
  """
  return 1.0 / (2 * D * (dx**-2 + dy**-2) + 15 * k * c0)

def validate_dt(dt, dx, dy, D, c0, k):
  print(f'dx={dx},dy={dy},D={D},c0={c0},k={k}')
  dt_upper_bound = get_upper_dt_bound(dx, dy, D, c0, k)

  if dt_upper_bound < dt:
    msg = f'error: given dt={dt:.04f} may produce unstable results! Use dt <= {dt_upper_bound:04f}.'
    print(msg)
  assert dt_upper_bound >= dt

def validate_solution(c):

  c1, c2, c3 = c

  if c1.min() < 0:
    id = np.unravel_index(c1.argmin(), c1.shape)
    print(f'c1 min: {c1.min()} at {id}')

  if c2.min() < 0:
    id = np.unravel_index(c2.argmin(), c2.shape)
    print(f'c2 min: {c2.min()} at {id}')

  if c3.min() < 0:
    id = np.unravel_index(c3.argmin(), c3.shape)
    print(f'c3 min: {c3.min()} at {id}')

  # material quantities over time
  q1 = np.sum(c1, axis=(1, 2))
  q2 = np.sum(c2, axis=(1, 2))
  q3 = np.sum(c3, axis=(1, 2))

  # rates of change of material quantities through time
  q1dt = np.diff(q1, 1, axis=0)
  q2dt = np.diff(q2, 1, axis=0)
  q3dt = np.diff(q3, 1, axis=0)

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
  assert np.all(c1 >= 0)
  assert np.all(q1dt <= sys.float_info.epsilon)

  assert np.all(c2 >= 0)
  assert np.all(q2dt <= sys.float_info.epsilon)

  # assert 3rd material quantity is non-negative and non-decreasing
  assert np.all(c3 >= 0)
  assert np.all(q3dt >= -sys.float_info.epsilon)

def stop(t, T, c1_init, c2_init, c1_last, c2_last, threshold):
  relative_quantity = (c1_last + c2_last).sum() / (c1_init + c2_init).sum()
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
  c0,
  k,
  c1_init,
  c2_init,
  c3_init,
  threshold,
  t_mix,
  T,
  dt):
  assert W > 0
  assert H > 0

  assert N > 0
  assert isinstance(N, int)

  assert M > 0
  assert isinstance(M, int)

  assert D >= 0

  assert np.all(c1_init >= 0)
  assert np.all(c2_init >= 0)
  assert np.all(c3_init >= 0)

  assert threshold is None or 0 <= threshold <= 1

  #assert t_mix is None or np.all(t_mix >= 0)

  assert T is None or (isinstance(T, int) and T > 0)

  assert threshold or T

  dx = W / (N - 1)
  dy = H / (M - 1)

  dt_upper_bound = get_upper_dt_bound(dx, dy, D, c0, k)
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
    print(f"Mixing times: {t_mix}")

def print_sim_debug_info(t, dt, c1_init, c2_init, c1_last, c2_last):
  q = (c1_last + c2_last).sum() / (c1_init + c2_init).sum()
  print(f'[t={t * dt:.02f},step={t}] q={q:.02f}')

def solvec(config, debug=False):
  W = config['W']
  H = config['H']
  N = config['N']
  M = config['M']
  D  = config['D']
  c0 = config['c0']
  k = config['k']
  t_mix = config['t_mix']
  threshold = config['threshold']
  B = config['B']
  T = config['T']
  dt = config['dt']
  frame_stride = config['frame_stride']
  optimal_mix = config['optimal_mix']

  c_init = get_larger_c_init(N, M, c0)

  return solve(W, H, N, M, D, c0, k, *c_init,
    threshold=threshold,
    t_mix=t_mix,
    B=B,
    debug=debug,
    T=T,
    dt=dt,
    frame_stride=frame_stride,
    optimal_mix=optimal_mix)

def solve(
  W,
  H,
  N,
  M,
  D,
  c0,
  k,
  c1_init,
  c2_init,
  c3_init,
  threshold=None,
  t_mix=None,
  B=2,
  debug=False,
  T=None,
  dt=None,
  frame_stride=1,
  optimal_mix=False):

  t_mix = None if t_mix is None else np.array(t_mix)
  validate_inputs(W, H, N, M, D, c0, k, c1_init, c2_init, c3_init, threshold, t_mix, T, dt)

  #print(W, H, N, M, D, c0, k, c1_init, c2_init, c3_init, threshold, t_mix, T, dt)

  dx = W / (N - 1)
  dy = H / (M - 1)
  dt_upper_bound = get_upper_dt_bound(dx, dy, D, c0, k)

  if debug:
    print_initial_debug_info(T, dt, dt_upper_bound, t_mix, threshold)

  filter = build_laplacian_filter(dx, dy)
  dt = dt or dt_upper_bound
  c1, c2, c3 = [ c1_init ], [ c2_init ], [ c3_init ]
  t = 0

  ts = [0]
  c1_last, c2_last, c3_last = c1[0], c2[0], c3[0]

  while True:

    if debug and t % 2000 == 0:
      print_sim_debug_info(t, dt, c1_init, c2_init, c1_last, c2_last)

    if t_mix is not None and np.any(abs(t * dt - t_mix) <= dt / 2): # and not mixing_done:
      if debug:
        print(f'[t={t * dt:.02f},step={t}] mixing')
      c1_last, c2_last, c3_last = mix(
        [c1_last, c2_last, c3_last], 
        B=B, 
        optimal_mix=optimal_mix, 
        debug=False)

    c1_next = c1_last + dt * (-3 * k * c1_last * c2_last + D * laplacian(c1_last, filter))
    c2_next = c2_last + dt * (-5 * k * c1_last * c2_last + D * laplacian(c2_last, filter))
    c3_next = c3_last + dt *   2 * k * c1_last * c2_last

    if t % frame_stride == 0:
      _ = c1.append(c1_next), c2.append(c2_next), c3.append(c3_next)

      # register that we calculated data for next time step
      ts.append(t + 1)

    # if T is not set, stop reaction when ratio of elements c1, c2
    # to the initial amount reaches threshold
    if stop(t, T, c1_init, c2_init, c1_last, c2_last, threshold):
      break

    # update time step
    t = t + 1
    # update last values
    c1_last, c2_last, c3_last = c1_next, c2_next, c3_next

  # convert python lists to numpy lists
  c1 = np.stack(c1, axis=0)
  c2 = np.stack(c2, axis=0)
  c3 = np.stack(c3, axis=0)

  # shape [ 3, t, width, height ]
  c = np.stack((c1, c2, c3), axis=0)
  #validate_solution(c)

  if debug:
    print(f'total time steps taken: {t}')
    print(f'saved result t: {c1.shape[0]}')

  return np.array(ts), c
