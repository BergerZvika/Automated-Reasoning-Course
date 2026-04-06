from pysmt.shortcuts import Symbol, And, Or, Not, Solver, ExactlyOne
from pysmt.typing import BOOL
import random


def generate_random_puzzle(clues=35):
    # Base valid solution (standard Sudoku template)
    base = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
    # Permute digits
    digits = list(range(1, 10))
    random.shuffle(digits)
    digit_map = {i + 1: digits[i] for i in range(9)}
    grid = [[digit_map[v] for v in row] for row in base]
    # Shuffle rows within each band of 3
    for band in range(3):
        rows = list(range(band * 3, band * 3 + 3))
        random.shuffle(rows)
        band_rows = [grid[r][:] for r in rows]
        for i, r in enumerate(range(band * 3, band * 3 + 3)):
            grid[r] = band_rows[i]
    # Shuffle cols within each band of 3
    for band in range(3):
        cols = list(range(band * 3, band * 3 + 3))
        perm = cols[:]
        random.shuffle(perm)
        for row in grid:
            orig = row[:]
            for i, c in enumerate(range(band * 3, band * 3 + 3)):
                row[c] = orig[perm[i]]
    # Remove cells to create puzzle
    puzzle = [row[:] for row in grid]
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    for i, j in cells[:81 - clues]:
        puzzle[i][j] = 0
    return puzzle


def sudoku_solver(puzzle):
    # Create Boolean variables x_i_j_d for each cell (i, j) and digit d
    cells = {(i, j, d): Symbol(f"x_{i}_{j}_{d}", BOOL) for i in range(9) for j in range(9) for d in range(1, 10)}

    # Define constraints
    constraints = []

    # Cell constraints: each cell contains exactly one digit
    for i in range(9):
        for j in range(9):
            constraints.append(ExactlyOne([cells[(i, j, d)] for d in range(1, 10)]))

    # Row constraints: each digit appears exactly once in each row
    for i in range(9):
        for d in range(1, 10):
            constraints.append(ExactlyOne([cells[(i, j, d)] for j in range(9)]))

    # Column constraints: each digit appears exactly once in each column
    for j in range(9):
        for d in range(1, 10):
            constraints.append(ExactlyOne([cells[(i, j, d)] for i in range(9)]))

    # Subgrid constraints: each digit appears exactly once in each 3x3 subgrid
    for block_i in range(3):
        for block_j in range(3):
            for d in range(1, 10):
                subgrid = [cells[(i, j, d)]
                           for i in range(block_i * 3, (block_i + 1) * 3)
                           for j in range(block_j * 3, (block_j + 1) * 3)]
                constraints.append(ExactlyOne(subgrid))

    # Initial clues from the puzzle
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:  # pre-filled cell with a number from 1 to 9
                d = puzzle[i][j]
                constraints.append(cells[(i, j, d)])

    # Solve the puzzle
    with Solver(name="z3") as solver:
        solver.add_assertion(And(constraints))
        if solver.solve():
            solution = [[0 for _ in range(9)] for _ in range(9)]
            for i in range(9):
                for j in range(9):
                    for d in range(1, 10):
                        if solver.get_value(cells[(i, j, d)]).is_true():
                            solution[i][j] = d
            return solution
        else:
            return None  # No solution found

puzzle = generate_random_puzzle(clues=35)

solution = sudoku_solver(puzzle)
if solution:
    print("SUDOKU_RESULT")
    for row in solution:
        print(" ".join(map(str, row)))
    print("---")
    for row in solution:
        print(row)
else:
    print("No solution exists.")
