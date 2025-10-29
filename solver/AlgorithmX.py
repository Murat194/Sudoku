from itertools import product

def solve_puzzle(puzzle_str):

    def encode(row, col, digit):
        return row * 81 + col * 9 + digit

    def decode(choice):
        digit = choice % 9
        col = (choice // 9) % 9
        row = choice // 81
        return row, col, digit

    constraints = []
    for r in range(9):
        for c in range(9):
            for d in range(9):
                cell = r * 9 + c
                rd = r * 9 + d
                cd = c * 9 + d
                bd = (r // 3 * 3 + c // 3) * 9 + d
                constraints.append([cell, 81 + rd, 162 + cd, 243 + bd])

    fixed = []
    for i, ch in enumerate(puzzle_str):
        if ch != '.':
            d = int(ch) - 1
            r, c = divmod(i, 9)
            fixed.append(encode(r, c, d))

    N = 324
    used_cols = set()
    solution = []

    col_to_rows = [[] for _ in range(N)]
    for i, cons in enumerate(constraints):
        for c in cons:
            col_to_rows[c].append(i)

    def search():
        if len(used_cols) == N:
            return True
        min_col = -1
        min_count = 1000
        for c in range(N):
            if c not in used_cols:
                count = sum(1 for r in col_to_rows[c] if all(x not in used_cols for x in constraints[r]))
                if count < min_count:
                    min_count = count
                    min_col = c
                if count == 0:
                    return False
        if min_col == -1:
            return False

        for r in col_to_rows[min_col]:
            if any(x in used_cols for x in constraints[r]):
                continue
            added = constraints[r]
            for x in added:
                used_cols.add(x)
            solution.append(r)
            if search():
                return True
            solution.pop()
            for x in added:
                used_cols.remove(x)
        return False

    for r in fixed:
        for c in constraints[r]:
            used_cols.add(c)
        solution.append(r)

    if search():
        result = ['.'] * 81
        for r in solution:
            row, col, digit = decode(r)
            result[row * 9 + col] = str(digit + 1)
        return ''.join(result)
    else:
        return None