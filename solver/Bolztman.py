import random
import math

def solve_puzzle(puzzle_str, max_steps=10000, initial_temp=1.0, cooling_rate=0.9995):
    digits = '123456789'
    board = [list(puzzle_str[i:i+9]) for i in range(0,81,9)]
    fixed = [[ch != '.' for ch in row] for row in board]

    for r in range(9):
        missing = [d for d in digits if d not in board[r]]
        blanks = [c for c in range(9) if not fixed[r][c]]
        random.shuffle(missing)
        for c, d in zip(blanks, missing):
            board[r][c] = d

    def conflicts(board):
        count = 0
        for c in range(9):
            col = [board[r][c] for r in range(9)]
            count += 9 - len(set(col))
        for br in range(0,9,3):
            for bc in range(0,9,3):
                block = [board[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]
                count += 9 - len(set(block))
        return count

    current_energy = conflicts(board)
    temp = initial_temp

    for step in range(max_steps):
        if current_energy == 0:
            return ''.join(''.join(row) for row in board)
        r = random.randint(0,8)
        blanks = [c for c in range(9) if not fixed[r][c]]
        if len(blanks) < 2:
            continue
        c1, c2 = random.sample(blanks, 2)
        board[r][c1], board[r][c2] = board[r][c2], board[r][c1]
        new_energy = conflicts(board)
        delta = new_energy - current_energy
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_energy = new_energy
        else:
            board[r][c1], board[r][c2] = board[r][c2], board[r][c1]
        temp *= cooling_rate
    return None 