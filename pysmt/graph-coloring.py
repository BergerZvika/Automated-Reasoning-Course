from pysmt.shortcuts import Symbol, And, Or, Not, Solver, ExactlyOne
from pysmt.typing import BOOL
import random


def graph_coloring_sat(vertex, edge, k):
    colors = range(k)

    # Boolean variable x_{v}_{c} = True if vertex v has color c
    vars = {(v, color): Symbol(f"{v}_{color}", BOOL) for v in vertex for color in colors}

    constraints = []

    # Each vertex gets exactly one color
    for v in vertex:
        constraints.append(ExactlyOne(vars[v, color] for color in colors))

    # Adjacent vertices must have different colors:
    # for each edge (v1, v2) and each color c, not both v1 and v2 can have color c
    for (v1, v2) in edge:
        for color in colors:
            constraints.append(Or(Not(vars[(v1, color)]), Not(vars[(v2, color)])))

    formula = And(constraints)

    with Solver(name="z3") as solver:
        solver.add_assertion(formula)
        if solver.solve():
            # Extract the assigned color for each vertex
            model = {v: None for v in vertex}
            for v in vertex:
                for color in colors:
                    if solver.get_value(vars[(v, color)]).is_true():
                        model[v] = color
            return model
        else:
            return None


def generate_random_pairs(num_pairs, n):
    """Generate num_pairs unique directed edges on vertices 0..n-1."""
    pairs = set()
    while len(pairs) < num_pairs:
        x1, x2 = random.randint(0, n-1), random.randint(0, n-1)
        if x1 != x2:
            pairs.add((x1, x2))
    return pairs


# Random graph: 7 vertices, 10 random edges, 3 colors
n = 7
vertex = list(range(n))
edge = generate_random_pairs(10, n)
k = 3

solution = graph_coloring_sat(vertex, edge, k)
if solution:
    print("GRAPH_COLORING_RESULT")
    print(f"N={n} K={k}")
    for v, color in solution.items():
        print(f"V {v} {color}")
    for v1, v2 in sorted(edge):
        print(f"E {v1} {v2}")
    print("---")
    print(f"Colored {n} vertices with {k} colors.")
    for v, color in solution.items():
        print(f"  vertex {v} -> color {color}")
else:
    print("No solution exists with the given number of colors.")
