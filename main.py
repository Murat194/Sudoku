import random
from copy import deepcopy

# ---------- Вспомогательные структуры (как в ваших скриншотах) ----------
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

# ---------- Решатель с backtracking (для проверки уникальности) ----------
def search(grid):
    """Возвращает решение или None, если решений 0 или >1."""
    if grid is None:
        return None
    if all(len(grid[s]) == 1 for s in squares):
        return grid
    # Выбираем клетку с минимальным числом кандидатов (>1)
    n, s = min((len(grid[s]), s) for s in squares if len(grid[s]) > 1)
    for d in grid[s]:
        result = search(assign(grid.copy(), s, d))
        if result:
            return result
    return None

def assign(grid, s, d):
    """Присваивает цифру d клетке s, удаляя d из всех пиров."""
    other_values = grid[s].replace(d, '')
    if all(eliminate(grid, s, d2) for d2 in other_values):
        return grid
    return None

def eliminate(grid, s, d):
    """Удаляет d из возможных значений клетки s."""
    if d not in grid[s]:
        return grid
    grid[s] = grid[s].replace(d, '')
    if len(grid[s]) == 0:
        return None  # Противоречие
    elif len(grid[s]) == 1:
        d2 = grid[s]
        if not all(eliminate(grid, s2, d2) for s2 in peers[s]):
            return None
    for u in units[s]:
        dplaces = [s2 for s2 in u if d in grid[s2]]
        if len(dplaces) == 0:
            return None
        elif len(dplaces) == 1:
            if not assign(grid, dplaces[0], d):
                return None
    return grid

def parse_grid(picture):
    """Преобразует строку в Grid (словарь {Square: DigitSet})."""
    grid = {s: digits for s in squares}
    for s, d in zip(squares, picture):
        if d in digits and not assign(grid, s, d):
            return None
    return grid

def grid_to_picture(grid):
    """Преобразует Grid в строку (для отображения)."""
    return ''.join(grid[s] if len(grid[s]) == 1 else '.' for s in squares)

# ---------- Генератор Судоку ----------
def generate_solved_grid():
    """Генерирует полное корректное решение Судоку."""
    grid = {s: digits for s in squares}
    shuffled_digits = list(digits)
    random.shuffle(shuffled_digits)
    # Начинаем с пустой сетки и заполняем случайно
    for s in squares:
        random.shuffle(shuffled_digits)
        for d in shuffled_digits:
            if d in grid[s]:
                if assign(grid, s, d):
                    break
    return search(grid)

def generate_puzzle(target_clues=30, max_attempts=1000):
    """
    Генерирует головоломку с target_clues подсказками и уникальным решением.
    target_clues: от 17 (макс. сложность) до ~60 (лёгкая)
    """
    solution = generate_solved_grid()
    if solution is None:
        raise RuntimeError("Не удалось сгенерировать решение.")
    
    puzzle = {s: solution[s] for s in squares}
    filled = list(squares)
    random.shuffle(filled)

    removed = 0
    attempts = 0
    while removed < (81 - target_clues) and attempts < max_attempts:
        s = filled[removed]
        backup = puzzle[s]
        puzzle[s] = digits  # временно делаем пустой

        # Проверяем, есть ли всё ещё уникальное решение
        test_grid = {k: v for k, v in puzzle.items()}
        sol1 = search(test_grid)
        if sol1 is None:
            # Без этой клетки решений нет — возвращаем
            puzzle[s] = backup
        else:
            # Проверяем, есть ли второе решение
            # Для этого временно удалим одну цифру из sol1 и проверим
            second_test = deepcopy(test_grid)
            # Попытка найти второе решение: меняем одну клетку и ищем снова
            found_second = False
            for sq in squares:
                if len(second_test[sq]) > 1:
                    for alt_d in second_test[sq]:
                        if alt_d != sol1[sq]:
                            trial = assign(deepcopy(second_test), sq, alt_d)
                            if trial and search(trial):
                                found_second = True
                                break
                    if found_second:
                        break
            if found_second:
                # Более одного решения — откат
                puzzle[s] = backup
            else:
                # Уникальное решение — можно удалять
                removed += 1
        attempts += 1

    return puzzle, solution
 
def format_sudoku_picture(puzzle_str): # функиция для вывода красивой картинки
    rows = [puzzle_str[i:i+9] for i in range(0, 81, 9)]

    top_line = "+-------+-------+-------+"
    mid_line = "|-------+-------+-------|"

    result = [top_line]
    for i, row in enumerate(rows):
        formatted_row = "| "
        for j, char in enumerate(row):
            formatted_row += char if char != '.' else '.'
            formatted_row += " "
            if j == 2 or j == 5:
                formatted_row += "| "
        formatted_row += "|"
        result.append(formatted_row)
        if i == 2 or i == 5:
            result.append(mid_line)

    result.append(top_line)
    return "\n".join(result)


if __name__ == "__main__":
    puzzle, solution = generate_puzzle(target_clues=25) # 25 подсказок
    print("Головоломка:")
    print(format_sudoku_picture(grid_to_picture(puzzle)))
    print("\nРешение:")
    print(format_sudoku_picture(grid_to_picture(solution)))