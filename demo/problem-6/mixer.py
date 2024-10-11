import numpy as np 

def mix_single(grid, rotations, new_loc_ids, subdivisions, debug):
  """Mix a single grid by splitting it in 4 
  equal parts by rotating and shuffling them.

  Args:
    grid (_type_): Grid to mix
  """
  block_size = np.array(grid.shape) / np.array(subdivisions)
  block_size = block_size.astype(int)

  if debug:
    print(block_size)

  # hx, hy = int(grid.shape[0] / 2), int(grid.shape[1] / 2)
  blocks = subdivisions[0] * subdivisions[1]
  block_grid = []
  for i in range(subdivisions[0]):
    left, right = i * block_size[0], block_size[0] * (i + 1) - 1
    block_columns = []
    for j in range(subdivisions[1]):
      top, bottom = j * block_size[1], block_size[1] * (j + 1) - 1
      block_columns.append(grid[left : right + 1, top : bottom + 1])
    block_grid.append(block_columns)

  block_grid = np.array(block_grid)

  if debug:
    print(block_grid)

  # blocks = [
  #   grid[:hx, :hy], # top left
  #   grid[hx:, hy:], # bottom right
  #   grid[hx:, :hy], # top right
  #   grid[:hx, hy:]  # bottom left
  # ]

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
    (subdivisions[0], subdivisions[1], *block_size)
  )

  if debug:
    print(blocks_grid)

  #return blocks_grid
  # put back together
  # upper_half = np.concatenate((blocks[0], blocks[2]), axis=0)
  # lower_half = np.concatenate((blocks[3], blocks[1]), axis=0)
  # return np.concatenate((upper_half, lower_half), axis=1)

  # concatinate coluns
  columns = np.concatenate(blocks_grid, axis=1)
  return np.concatenate(columns, axis=1)

def mix(
  grids, 
  rotate=True, 
  shuffle=True, 
  subdivisions=(2, 2), 
  debug=False):

  assert subdivisions[0] > 1
  assert subdivisions[1] > 1

  for grid in grids:
    for i, length in enumerate(grid.shape):
      assert length % subdivisions[i] == 0

  # generate random rotations for subdivisions of the grid
  blocks = subdivisions[0] * subdivisions[1]
  rotations = np.random.randint(4, size=blocks) if rotate else np.zeros(blocks)
  # random permutation of blocks
  block_order = np.random.permutation(blocks) if shuffle else np.arange(0, blocks)

  # best theoretical mix for 2x2
  # if (2, 2) == subdivisions:
  #   rotations = [0, 0, 0, 0]
  #   block_order = [1, 0, 3, 2]

  # mix each block
  return [ mix_single(g, rotations, block_order, subdivisions, debug) for g in grids ]