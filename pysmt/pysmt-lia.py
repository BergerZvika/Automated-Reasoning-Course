from pysmt.shortcuts import Solver, Symbol, Plus, Equals, Int, Real
from pysmt.typing import INT, REAL, BOOL

x = Symbol("x", INT)
y = Symbol("y", REAL)

formula1 = Equals(Plus(x, Int(5)), Int(10))
formula2 = y < Real(5.0)
formula3 = y > Real(4.0)

with Solver(name="z3") as solver:
    solver.add_assertion(formula1)
    solver.add_assertion(formula2)
    solver.add_assertion(formula3)

    if solver.solve():
        model = solver.get_model()
        print(model)
    else:
        print("No solution exists")



