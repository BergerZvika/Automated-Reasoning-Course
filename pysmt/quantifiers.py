from pysmt.shortcuts import Solver, Symbol, Plus, Int, ForAll, Plus, LT
from pysmt.typing import INT

x = Symbol("x", INT)

formula = ForAll([x], LT(Plus(x, Int(1)), x))
print(formula)

solver = Solver(name="z3")
solver.add_assertion(formula)
r = solver.check_sat()
print("result: ", r)









