import numpy as np 

def mix_single(grid, rotations, new_loc_ids, B, debug):
  
  block_size = np.array(grid.shape) / B
  block_size = block_size.astype(int)

  if debug:
    print(block_size)

  blocks = B ** 2
  block_grid = []
  for i in range(B):
    left, right = i * block_size[0], block_size[0] * (i + 1) - 1
    block_columns = []
    for j in range(B):
      top, bottom = j * block_size[1], block_size[1] * (j + 1) - 1
      block_columns.append(grid[left : right + 1, top : bottom + 1])
    block_grid.append(block_columns)

  block_grid = np.array(block_grid)

  if debug:
    print(block_grid)

  # reshape grid of blocks to rotate and reindex
  blocks_1d = np.reshape(block_grid, (blocks, *block_size))

  if debug:
    print(blocks_1d)

  # rotate
  blocks_1d = np.array([ np.rot90(b, k) for b, k in zip(blocks_1d, rotations) ])

  # shuffle
  blocks_1d = blocks_1d[new_loc_ids]  

  # reshape back into a grid
  blocks_grid = np.reshape(
    blocks_1d, 
    (B, B, *block_size)
  )

  if debug:
    print(blocks_grid)

  # concatenate columns and rows back into N x M matrix 
  columns = np.concatenate(blocks_grid, axis=1)
  return np.concatenate(columns, axis=1)

def mix(
  grids, 
  rotate=True, 
  shuffle=True, 
  B=2, 
  debug=False):

  assert B > 1

  for grid in grids:
    for length in grid.shape:
      assert length % B == 0

  # generate random rotations for subdivisions of the grid
  blocks = B ** 2
  rotations = np.random.randint(4, size=blocks) if rotate else np.zeros(blocks)
  # random permutation of blocks
  block_order = np.random.permutation(blocks) if shuffle else np.arange(0, blocks)

  # best theoretical mix for 2x2
  # if 2 == B:
  #   rotations = np.array([0, 0, 0, 0])
  #   block_order = np.array([3, 2, 1, 0])

  # mix each block
  return [ mix_single(g, rotations, block_order, B, debug) for g in grids ]