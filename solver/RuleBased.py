from copy import deepcopy
from solver.Backtracking import solve as backtracking_solve, grid_to_string as bt_to_str

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

def apply_constraints(grid):
    changed = True
    while changed:
        changed = False
        for s in squares:
            if len(grid[s]) == 1:
                d = grid[s]
                for p in peers[s]:
                    if d in grid[p]:
                        grid[p] = grid[p].replace(d, '')
                        if len(grid[p]) == 0:
                            return False  
                        changed = True

        for u in unitlist:
            for d in digits:
                places = [s for s in u if d in grid[s]]
                if len(places) == 0:
                    return False 
                elif len(places) == 1:
                    s = places[0]
                    if len(grid[s]) > 1:
                        grid[s] = d
                        changed = True
    return True

def is_solved(grid):
    return all(len(grid[s]) == 1 for s in squares)

def solve_puzzle(puzzle_str, use_backtrack_fallback=True):
    grid = {s: (d if d != '.' else digits) for s, d in zip(squares, puzzle_str)}

    consistent = apply_constraints(grid)
    if not consistent:
        return None 
    if is_solved(grid):
        return ''.join(grid[s] for s in squares)
    if use_backtrack_fallback:
        solved_grid = backtracking_solve(deepcopy(grid))
        if solved_grid:
            return bt_to_str(solved_grid)
        else:
            return None
    else:
        return None