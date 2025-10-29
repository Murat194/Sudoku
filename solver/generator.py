import random
from copy import deepcopy
from solvers.Backtracking import solve as bt_solve, parse_grid, grid_to_string

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

def generate_solved_grid():
    """Генерирует полностью заполненное корректное судоку."""
    grid = {s: digits for s in squares}
    shuffled_digits = list(digits)
    random.shuffle(shuffled_digits)
    for s in squares:
        random.shuffle(shuffled_digits)
        for d in shuffled_digits:
            if d in grid[s]:
                # Простая эвристика: пробуем присвоить
                new_grid = assign(grid.copy(), s, d)
                if new_grid is not None:
                    grid = new_grid
                    break
    return bt_solve(grid)

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
        val = grid[s]
        if not all(eliminate(grid, peer, val) for peer in peers[s]):
            return None
    for u in units[s]:
        places = [sq for sq in u if d in grid[sq]]
        if len(places) == 0:
            return None
        elif len(places) == 1:
            if not assign(grid, places[0], d):
                return None
    return grid

def count_solutions(puzzle_str, limit=2):
    """Возвращает количество решений (до limit)."""
    solutions = []
    _collect_solutions(parse_grid(puzzle_str), solutions, limit)
    return len(solutions)

def _collect_solutions(grid, results, limit):
    if len(results) >= limit:
        return
    if grid is None:
        return
    if all(len(grid[s]) == 1 for s in squares):
        results.append(grid_to_string(grid))
        return
    n, s = min((len(grid[s]), s) for s in squares if len(grid[s]) > 1)
    for d in grid[s]:
        _collect_solutions(assign(deepcopy(grid), s, d), results, limit)

def generate_puzzle(num_clues=30):
    """
    Генерирует валидную головоломку с ровно num_clues подсказками.
    Минимум: 17, максимум: 71.
    """
    if not (17 <= num_clues <= 81):
        raise ValueError("Количество подсказок должно быть от 17 до 81")
    
    solution_grid = generate_solved_grid()
    if solution_grid is None:
        raise RuntimeError("Не удалось сгенерировать решение")

    puzzle = {s: solution_grid[s] for s in squares}
    filled = list(squares)
    random.shuffle(filled)
    removed = 0
    attempts = 0
    max_attempts = 2000

    while removed < (81 - num_clues) and attempts < max_attempts:
        s = filled[removed]
        backup = puzzle[s]
        puzzle[s] = digits  # делаем пустой

        puzzle_str = ''.join(puzzle[sq] if len(puzzle[sq]) == 1 else '.' for sq in squares)
        sol_count = count_solutions(puzzle_str, limit=2)

        if sol_count != 1:
            puzzle[s] = backup  # возврат — решение не уникально
        else:
            removed += 1
        attempts += 1

    final_puzzle_str = ''.join(puzzle[s] if len(puzzle[s]) == 1 else '.' for s in squares)
    solution_str = grid_to_string(solution_grid)
    return final_puzzle_str, solution_str