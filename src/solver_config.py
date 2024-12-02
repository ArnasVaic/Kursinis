solver_config = {
  'W': 1.0,
  'H': 1.0,
  'N': 80,
  'M': 80,
  'D': 1e-4,
  'k': 1,
  'c0': 1,
  't_mix': None,
  'B': 2,
  'T': 360000,
  'dt': 0.00001,
  'frame_stride': 1800
}

def solver_config_id():
  N, M = solver_config['N'], solver_config['M']
  D = solver_config['D']
  k = solver_config['k']
  c0 = solver_config['c0']
  dt = solver_config['dt']
  return f'[N,M,D,k,c0,dt]=[{N},{M},{D},{k},{c0},{dt}]'
