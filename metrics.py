import time
import tracemalloc

def evaluate_solver(solver_func, solver_name, puzzle_str, solution_str=None):
    tracemalloc.start()
    start_time = time.perf_counter()

    try:
        result = solver_func(puzzle_str)
        success = result is not None
        correct = success and (solution_str is None or result == solution_str)
    except Exception as e:
        result = None
        success = False
        correct = False

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("- ", solver_name)
    print("- ", str(round(end_time - start_time, 6)), " сек")
    print("- ", str(peak / 1024), " КБ")
    print("- Answer: ", str(correct))
    print("------------------------------")

    return {
        "solver": solver_name,
        "success": success,
        "correct": correct,
        "time_sec": end_time - start_time,
        "memory_kb": peak / 1024,
        "result": result
    }