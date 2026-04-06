import warnings
from pysmt.shortcuts import Symbol, And, Equals, Int, is_sat, Portfolio
from pysmt.typing import BOOL, INT
from pysmt.logics import QF_BOOL

def main():
    # Create Boolean and Integer Symbols
    A = Symbol("A", BOOL)
    B = Symbol("B", BOOL)

    # Build a formula
    formula = And(A, B)

    # Use a Portfolio solver strategy
    # (suppress pysmt's "Defining new symbol" warnings — harmless in Portfolio)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="pysmt")
        with Portfolio(["z3"], logic=QF_BOOL) as solver:
            solver.add_assertion(formula)

            # Check satisfiability
            if solver.solve():
                model = solver.get_model()
                print("Satisfiable! The model is:\n", model)
            else:
                print("Unsatisfiable!")

if __name__ == '__main__':
    main()
