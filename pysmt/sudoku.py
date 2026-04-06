from pysmt.shortcuts import Symbol, And, Or, Not, Solver, ExactlyOne
from pysmt.typing import BOOL

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

# Example usage
# # Puzzle 1
# puzzle = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ]

# Puzzle 2
puzzle = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

# Puzzle 3
# puzzle = [
#     [0, 0, 0, 0, 0, 7, 0, 0, 9],
#     [0, 0, 4, 0, 6, 0, 3, 0, 0],
#     [0, 6, 0, 5, 0, 0, 4, 0, 0],
#     [0, 9, 0, 0, 5, 1, 0, 0, 6],
#     [5, 0, 0, 8, 0, 3, 0, 0, 7],
#     [6, 0, 0, 9, 2, 0, 0, 8, 0],
#     [0, 0, 8, 0, 0, 9, 0, 2, 0],
#     [0, 0, 1, 0, 8, 0, 9, 0, 0],
#     [3, 0, 0, 4, 0, 0, 0, 0, 0]
# ]

# Puzzle 4
# puzzle = [
#     [0, 0, 0, 7, 0, 0, 3, 0, 0],
#     [8, 0, 0, 0, 0, 4, 0, 0, 5],
#     [0, 0, 0, 0, 0, 0, 6, 0, 0],
#     [5, 0, 1, 0, 3, 0, 9, 0, 0],
#     [0, 4, 0, 0, 0, 0, 0, 5, 0],
#     [0, 0, 9, 0, 7, 0, 2, 0, 8],
#     [0, 0, 8, 0, 0, 0, 0, 0, 0],
#     [6, 0, 0, 4, 0, 0, 0, 0, 1],
#     [0, 0, 2, 0, 0, 1, 0, 0, 0]
# ]

# Puzzle 5
# puzzle = [
#     [0, 0, 0, 8, 0, 0, 0, 0, 1],
#     [0, 0, 4, 0, 0, 0, 0, 2, 0],
#     [0, 2, 0, 7, 1, 0, 0, 0, 0],
#     [0, 4, 3, 0, 0, 0, 0, 0, 8],
#     [9, 0, 0, 0, 0, 0, 0, 0, 3],
#     [6, 0, 0, 0, 0, 0, 2, 9, 0],
#     [0, 0, 0, 0, 4, 8, 0, 3, 0],
#     [0, 9, 0, 0, 0, 0, 5, 0, 0],
#     [8, 0, 0, 0, 0, 5, 0, 0, 0]
# ]

# Puzzle 6
# puzzle = [
#     [2, 0, 0, 0, 0, 0, 0, 0, 5],
#     [0, 0, 7, 0, 3, 0, 2, 0, 0],
#     [0, 6, 0, 8, 0, 2, 0, 4, 0],
#     [0, 0, 8, 1, 0, 5, 4, 0, 0],
#     [0, 2, 0, 4, 0, 6, 0, 3, 0],
#     [0, 0, 3, 7, 0, 8, 1, 0, 0],
#     [0, 1, 0, 6, 0, 9, 0, 8, 0],
#     [0, 0, 2, 0, 5, 0, 6, 0, 0],
#     [6, 0, 0, 0, 0, 0, 0, 0, 3]
# ]

# Puzzle 7
# puzzle = [
#     [0, 0, 0, 6, 0, 0, 0, 0, 0],
#     [0, 7, 0, 0, 9, 0, 2, 0, 5],
#     [0, 0, 8, 0, 0, 1, 0, 6, 0],
#     [0, 5, 0, 1, 0, 0, 8, 0, 0],
#     [6, 0, 3, 0, 0, 0, 5, 0, 1],
#     [0, 0, 7, 0, 0, 4, 0, 2, 0],
#     [0, 3, 0, 4, 0, 0, 7, 0, 0],
#     [7, 0, 6, 0, 1, 0, 0, 5, 0],
#     [0, 0, 0, 0, 0, 7, 0, 0, 0]
# ]

# Puzzle 8
# puzzle = [
#     [0, 0, 0, 0, 5, 0, 0, 0, 0],
#     [0, 0, 7, 1, 0, 0, 0, 0, 3],
#     [3, 0, 2, 0, 0, 0, 4, 0, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 2],
#     [0, 0, 1, 0, 0, 0, 3, 0, 0],
#     [9, 0, 0, 0, 2, 0, 0, 0, 4],
#     [0, 0, 4, 0, 0, 0, 1, 0, 9],
#     [2, 0, 0, 0, 0, 8, 7, 0, 0],
#     [0, 0, 0, 0, 3, 0, 0, 0, 0]
# ]

# Puzzle 9
# puzzle = [
#     [0, 0, 0, 0, 8, 0, 0, 0, 6],
#     [9, 0, 0, 0, 5, 0, 1, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0, 0, 0],
#     [0, 7, 0, 0, 0, 9, 0, 4, 0],
#     [0, 5, 0, 7, 0, 1, 0, 6, 0],
#     [0, 4, 0, 8, 0, 0, 0, 2, 0],
#     [0, 0, 0, 0, 0, 5, 0, 0, 0],
#     [0, 0, 1, 0, 2, 0, 0, 0, 4],
#     [5, 0, 0, 0, 9, 0, 0, 0, 0]
# ]

# Puzzle 10
# puzzle = [
#     [0, 0, 0, 0, 0, 7, 0, 8, 0],
#     [6, 0, 0, 0, 0, 0, 4, 0, 3],
#     [0, 0, 0, 2, 0, 0, 0, 5, 9],
#     [0, 0, 0, 8, 4, 0, 0, 0, 0],
#     [4, 0, 6, 0, 0, 0, 2, 0, 7],
#     [0, 0, 0, 0, 9, 1, 0, 0, 0],
#     [2, 6, 0, 0, 0, 3, 0, 0, 0],
#     [1, 0, 8, 0, 0, 0, 0, 0, 4],
#     [0, 7, 0, 9, 0, 0, 0, 0, 0]
# ]


# hard
# puzzle = [
#     [0, 0, 4, 1, 2, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 4, 0, 1, 6],
#     [0, 3, 0, 0, 5, 0, 0, 0, 9],
#     [0, 0, 0, 4, 0, 2, 8, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 3, 5, 7, 0],
#     [5, 0, 0, 8, 0, 0, 0, 0, 0],
#     [6, 0, 2, 0, 1, 0, 0, 0, 0],
#     [4, 0, 0, 0, 0, 7, 9, 0, 0]
# ]

solution = sudoku_solver(puzzle)
if solution:
    for row in solution:
        print(row)
else:
    print("No solution exists.")
