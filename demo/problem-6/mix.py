import numpy as np 

def mix_single(grid, rotations, new_loc_ids):
  """Mix a single grid by splitting it in 4 
  equal parts by rotating and shuffling them.

  Args:
    grid (_type_): Grid to mix
  """
  hx, hy = int(grid.shape[0] / 2), int(grid.shape[1] / 2)

  blocks = [
    grid[:hx, :hy], # top left
    grid[hx:, hy:], # bottom right
    grid[hx:, :hy], # top right
    grid[:hx, hy:]  # bottom left
  ]

  # rotate
  blocks = np.array([ np.rot90(b, k) for b, k in zip(blocks, rotations) ])

  # shuffle
  blocks = blocks[new_loc_ids]  

  # put back together
  upper_half = np.concatenate((blocks[0], blocks[2]), axis=0)
  lower_half = np.concatenate((blocks[3], blocks[1]), axis=0)
  return np.concatenate((upper_half, lower_half), axis=1)

def mix(grids):
  """Mix multiple grids with the same transformations by 
  splitting it in 4 equal parts by rotating and shuffling them.

  Args:
      grid (_type_): Grids to mix.
  """
  # generate random rotations for 4 subdivisions of the grid
  rotations = np.random.randint(4, size=4)
  # random permutation of 4 blocks
  block_order = np.random.permutation(4)
  # mix each block
  return [ mix_single(g, rotations, block_order) for g in grids ]