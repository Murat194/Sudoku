from generator import generate_puzzle
from solver.Backtracking import solve_puzzle as solve1
from solver.RuleBased import solve_puzzle as solve2
from solver.Bolztman import solve_puzzle as solve3
from solver.AlgorithmX import solve_puzzle as solve4
from metrics import evaluate_solver

def format_sudoku_picture(puzzle_str):
    if puzzle_str is None:
        return "Нет решения"
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
    puzzle_str, solution_str = generate_puzzle(num_clues=81) 
    # num_clues = количество подсказок = сложность (минимум 17, максимум 81)
    
    print("sudoku:")
    print(format_sudoku_picture(puzzle_str))
    print("\nsolve:")
    print(format_sudoku_picture(solution_str))

    evaluate_solver(solve1, "backtracking", puzzle_str, solution_str)
    evaluate_solver(solve2, "rulebased", puzzle_str, solution_str)
    evaluate_solver(solve3, "boltzman", puzzle_str, solution_str)
    evaluate_solver(solve4, "algorithmx", puzzle_str, solution_str)
