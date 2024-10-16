solver_config = {
  'W': 1.0,
  'H': 1.0,
  'dx': 1.0/99.1,
  'dy': 1.0/99.1,
  'D': 0.0001,
  't_mix': 500,
  'B': 4,
  'out_stride': 1
}

def solver_config_id():
  W, H = solver_config['W'], solver_config['H']
  dx, dy = solver_config['dx'], solver_config['dy']
  D = solver_config['D']
  N, M = int(W / dx) + 1, int(H / dy) + 1
  return f'[N,M,D]=[{N},{M},{D}]'