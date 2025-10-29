from copy import deepcopy

digits = '123456789'
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    return [a + b for a in A for b in B]

squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = {s: [u for u in unitlist if s in u] for s in squares}
peers = {s: set(sum(units[s], [])) - {s} for s in squares}

def parse_grid(picture):
    grid = {s: digits for s in squares}
    for s, d in zip(squares, picture):
        if d in digits and not assign(grid, s, d):
            return None
    return grid

def grid_to_string(grid):
    return ''.join(grid[s] if len(grid[s]) == 1 else '.' for s in squares)

def assign(grid, s, d):
    other_vals = grid[s].replace(d, '')
    if all(eliminate(grid, s, x) for x in other_vals):
        return grid
    return None

def eliminate(grid, s, d):
    if d not in grid[s]:
        return grid
    grid[s] = grid[s].replace(d, '')
    if len(grid[s]) == 0:
        return None
    elif len(grid[s]) == 1:
        d2 = grid[s]
        if not all(eliminate(grid, peer, d2) for peer in peers[s]):
            return None
    for u in units[s]:
        dplaces = [sq for sq in u if d in grid[sq]]
        if len(dplaces) == 0:
            return None
        elif len(dplaces) == 1:
            if not assign(grid, dplaces[0], d):
                return None
    return grid

def solve(grid):
    if grid is None:
        return None
    if all(len(grid[s]) == 1 for s in squares):
        return grid
    n, s = min((len(grid[s]), s) for s in squares if len(grid[s]) > 1)
    for d in grid[s]:
        result = solve(assign(deepcopy(grid), s, d))
        if result:
            return result
    return None

def solve_puzzle(puzzle_str):
    grid = parse_grid(puzzle_str)
    solved = solve(grid)
    return grid_to_string(solved) if solved else None