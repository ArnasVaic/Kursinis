solver_config = {
  'W': 2.154434690031884,
  'H': 2.154434690031884,
  'N': 80,
  'M': 80,
  'D': 28e-6,
  'k': 192,
  'c0': 1e-6,
  't_mix': None,
  'B': 2,
  'T': 10000,
  'dt': None,
  'frame_stride': 50
}

def solver_config_id():
  N, M = solver_config['N'], solver_config['M']
  D = solver_config['D']
  k = solver_config['k']
  c0 = solver_config['c0']
  dt = solver_config['dt']
  return f'[N,M,D,k,c0,dt]=[{N},{M},{D},{k},{c0},{dt}]'
