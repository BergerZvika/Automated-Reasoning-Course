from pysmt.shortcuts import Symbol, And, Solver
from pysmt.typing import BOOL

A = Symbol("A", BOOL)
B = Symbol("B", BOOL)
formula = And(A, B)

# Try solvers in order — use the first available one
for solver_name in ["z3", "cvc5"]:
    try:
        with Solver(name=solver_name) as solver:
            solver.add_assertion(formula)
            if solver.solve():
                print(f"SAT  (solver: {solver_name})")
                print("A =", solver.get_value(A))
                print("B =", solver.get_value(B))
            else:
                print(f"UNSAT  (solver: {solver_name})")
            break
    except Exception:
        print(f"{solver_name} not available, trying next...")
