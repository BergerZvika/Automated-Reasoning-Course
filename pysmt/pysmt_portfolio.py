import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # suppress Portfolio internal warnings

from pysmt.shortcuts import Symbol, And, Not, Or, Solver, Portfolio
from pysmt.typing import BOOL
from pysmt.logics import QF_BOOL

# Portfolio is designed for checking satisfiability across multiple solvers.
# Model extraction (get_value) is unreliable in Portfolio due to internal
# symbol renaming — use a regular Solver when you need a model.

A = Symbol("A", BOOL)
B = Symbol("B", BOOL)

# --- Portfolio: SAT check only ---
for formula, label in [
    (And(A, B),       "And(A, B)"),
    (And(A, Not(A)),  "And(A, Not(A))"),
    (Or(A, B),        "Or(A, B)"),
]:
    with Portfolio(["z3", "cvc5"], logic=QF_BOOL) as solver:
        solver.add_assertion(formula)
        result = "SAT" if solver.solve() else "UNSAT"
        print(f"{label:20s} -> {result}")

# --- Regular Solver: model extraction ---
print()
with Solver(name="z3") as solver:
    solver.add_assertion(And(A, B))
    if solver.solve():
        print("And(A, B) model:  A =", solver.get_value(A), " B =", solver.get_value(B))
