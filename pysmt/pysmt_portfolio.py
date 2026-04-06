import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # suppress Portfolio internal warnings

from pysmt.shortcuts import Symbol, And, Portfolio
from pysmt.typing import BOOL
from pysmt.logics import QF_BOOL

def main():
    A = Symbol("A", BOOL)
    B = Symbol("B", BOOL)

    formula = And(A, B)

    with Portfolio(["z3", "cvc5"], logic=QF_BOOL) as solver:
        solver.add_assertion(formula)

        if solver.solve():
            print("Satisfiable!")
            print("A =", solver.get_value(A))
            print("B =", solver.get_value(B))
        else:
            print("Unsatisfiable")

if __name__ == '__main__':
    main()
