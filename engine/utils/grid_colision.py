def is_wall(grid, x, y):

    tx = int(x)
    ty = int(y)

    if tx < 0 or ty < 0:
        return True

    if tx >= grid.shape[1]:
        return True

    if ty >= grid.shape[0]:
        return True

    return grid[ty, tx] != 0


