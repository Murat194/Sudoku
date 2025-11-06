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

# 1. Naked Single
# Если в клетке осталась только одна возможная цифра, то она и есть правильный ответ для этой клетки.
        for s in squares:
            if len(grid[s]) == 1:
                d = grid[s]
                for p in peers[s]:
                    if d in grid[p]:
                        grid[p] = grid[p].replace(d, '')
                        if len(grid[p]) == 0:
                            return False
                        changed = True

# 2. Naked Pairs - 07.11.25
# Если в юните две клетки имеют одинаковые 2 кандидата, 
# и больше нигде в юните они не встречаются, то убираем эти 2 кандидата из всех других клеток юнита.
        for u in unitlist:
            pairs = {}
            for s in u:
                if len(grid[s]) == 2:
                    key = tuple(sorted(grid[s]))
                    if key not in pairs:
                        pairs[key] = []
                    pairs[key].append(s)
            for key, squares_with_pair in pairs.items():
                if len(squares_with_pair) == 2:
                    d1, d2 = key
                    for s in u:
                        if s not in squares_with_pair and (d1 in grid[s] or d2 in grid[s]):
                            old_len = len(grid[s])
                            grid[s] = grid[s].replace(d1, '').replace(d2, '')
                            if len(grid[s]) == 0:
                                return False
                            if len(grid[s]) != old_len:
                                changed = True

# 3. Hidden Single
# Если в юните цифра возможна только в одной клетке, то она и есть правильный ответ для этой клетки.
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

# 4. Hidden Pairs - 07.11.25
# Если в юните есть 2 цифры, которые возможны только в 2 клетках,
# и больше нигде в юните, то убираем из этих 2 клеток все другие кандидаты.
        for u in unitlist:
            digit_places = {d: [s for s in u if d in grid[s]] for d in digits}
            for i, d1 in enumerate(digits):
                places1 = digit_places[d1]
                if len(places1) == 2:
                    for d2 in digits[i+1:]:
                        places2 = digit_places[d2]
                        if len(places2) == 2 and set(places1) == set(places2):
                            s1, s2 = places1
                            new_candidates = d1 + d2
                            if grid[s1] != new_candidates:
                                grid[s1] = new_candidates
                                changed = True
                            if grid[s2] != new_candidates:
                                grid[s2] = new_candidates
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

