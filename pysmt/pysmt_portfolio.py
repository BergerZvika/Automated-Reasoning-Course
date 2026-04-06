import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from pysmt.shortcuts import Symbol, And, Portfolio
from pysmt.typing import BOOL
from pysmt.logics import QF_BOOL

A = Symbol("A", BOOL)
B = Symbol("B", BOOL)

with Portfolio(["z3", "cvc5"], logic=QF_BOOL) as solver:
    solver.add_assertion(And(A, B))
    if solver.solve():
        print("SAT")
    else:
        print("UNSAT")
