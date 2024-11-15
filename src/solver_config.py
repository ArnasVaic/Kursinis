solver_config = {
  'W': 1.0,
  'H': 1.0,
  'N': 100,
  'M': 100,
  'D': 1e-4,
  'k': 1,
  'c0': 1,
  't_mix': None,
  'B': 2,
  'T': None,
  'dt': None
}

def solver_config_id():
  N, M = solver_config['N'], solver_config['M']
  D = solver_config['D']
  k = solver_config['k']
  c0 = solver_config['c0']
  return f'[N,M,D,k,c0]=[{N},{M},{D},{k},{c0}]'