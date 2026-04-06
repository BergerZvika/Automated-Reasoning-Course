from pysmt.shortcuts import Symbol, And, Or, Not, Solver, ExactlyOne
from pysmt.typing import BOOL
import random


def graph_coloring_sat(vertex, edge, k):
    # Step 1: Define Boolean variables for each v-color combination
    colors = range(k)
    vars = {(v, color): Symbol(f"{v}_{color}", BOOL) for v in vertex for color in colors}

    constraints = []

    # Step 2: Ensure each v has exactly one color
    # for v in vertex:
    #     # At least one color for each v
    #     constraints.append(Or([vars[(v, color)] for color in colors]))
    #
    #     # At most one color for each v
    #     for color1 in colors:
    #         for color2 in colors:
    #             if color1 < color2:
    #                 constraints.append(Or(Not(vars[(v, color1)]), Not(vars[(v, color2)])))

    for v in vertex:
        constraints.append(ExactlyOne(vars[v, color] for color in colors))

    # Step 3: Adjacent vertex must not have the same color
    for (v1, v2) in edge:
        for color in colors:
            constraints.append(Or(Not(vars[(v1, color)]), Not(vars[(v2, color)])))

    # Step 4: Combine all constraints
    formula = And(constraints)

    # Step 5: Use a SAT solver to find a solution
    with Solver(name="z3") as solver:
        solver.add_assertion(formula)
        if solver.solve():
            # If satisfiable, extract solution
            model = {v: None for v in vertex}
            for v in vertex:
                for color in colors:
                    if solver.get_value(vars[(v, color)]).is_true():
                        model[v] = color
            return model
        else:
            return None

# Example 1
# vertex = ["A", "B", "C", "D"]
# edge = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "D"), ("A", "C")]
# k = 3  # Use three colors

# Example presentation
# vertex = [x + 1 for x in range(7)]
# edge = [(1, 4), (1, 5), (1, 6), (4, 6), (5, 6), (6, 7), (4, 2), (5, 3), (2, 7), (2, 3), (3, 7)]
# k = 3  # Use three colors

# BIG Example
def generate_random_pairs(num_pairs,n):
    pairs = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(num_pairs)]
    pairs = set(pairs)
    pairs = [(x1,x2) for (x1,x2) in pairs if x1 != x2]
    return pairs

n = 7
vertex = list(range(n))
edge = generate_random_pairs(10, n)
k = 3


solution = graph_coloring_sat(vertex, edge, k)
if solution:
    print("Solution found:")
    for v, color in solution.items():
        print(f"vertex {v} has color {color}")
else:
    print(f"No solution exists with the given number of colors.")

