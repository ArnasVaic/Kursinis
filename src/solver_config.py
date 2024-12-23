solver_config = {

  # frame stride
  'frame_stride': 10,

  # time step
  'dt': None,

  # reaction parameters
  'W': 2 * 2.154434690031884,
  'H': 2 * 2.154434690031884,
  'N': 2 * 80,
  'M': 2 * 80,
  'D': 28e-6,
  'k': 192,
  'c0': 1e-6,
  
  # stop condition
  'threshold': 0.03,
  'T': None,
  
  # mixing parameters
  'B': 4,
  't_mix': None, #[0],
  'optimal_mix': True, # no effect on larger configurations
}

def solver_config_id():
  N, M = solver_config['N'], solver_config['M']
  D = solver_config['D']
  k = solver_config['k']
  c0 = solver_config['c0']
  dt = solver_config['dt']
  return f'[N,M,D,k,c0,dt]=[{N},{M},{D},{k},{c0},{dt}]'
