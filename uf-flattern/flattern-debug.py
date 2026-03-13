# importing system module for reading files
import sys

# import classes for parsing smt2 files
from pysmt.smtlib.parser import SmtLibParser
from six.moves import cStringIO
from pysmt.walkers import IdentityDagWalker
from pysmt.walkers.generic import handles
import pysmt.operators as op
from pysmt.shortcuts import get_env

# import pysmt functions for creating formulas and terms
from pysmt.shortcuts import Not, EqualsOrIff, Function, And, Symbol, BOOL


class SubTermsGetter(IdentityDagWalker):
    def __init__(self, env):
        IdentityDagWalker.__init__(self, env=env, invalidate_memoization=True)
        self.sub_terms = set([])

    @handles(set(op.ALL_TYPES))
    def walk_collect(self, formula, args, **kwargs):
        self.sub_terms.add(formula)

# get all terms in a cube.
# for example: get_terms([x=y, f(x)=z]) = [x, y, z, f(x)]
def get_terms(cube):
  formula = And(cube)
  sub_terms_getter = SubTermsGetter(get_env())
  sub_terms_getter.walk(formula)
  return [t for t in sub_terms_getter.sub_terms if t.is_symbol() or t.is_function_application()]

# check if `cube` is indeed a cube (that is, a list of literals)
def is_cube(cube):
  for lit in cube:
    if not is_lit(lit):
      return False
  return True

# check if `term` is a literal (equality or negation of equality)
def is_lit(term):
  return term.is_equals() or \
         (term.is_not() and (term.args()[0].is_equals() or (term.args()[0].is_function_application() and term.args()[0].get_type() == BOOL))) or \
         (term.is_function_application() and term.get_type() == BOOL)

def is_flat_lit(lit):
    assert is_lit(lit)

    if lit.is_equals():
        left, right = lit.args()
        return left.is_symbol() and (right.is_symbol() or
                                     (right.is_function_application() and all(arg.is_symbol() for arg in right.args())))

    elif lit.is_not() and lit.args()[0].is_equals():
        left, right = lit.args()[0].args()
        return left.is_symbol() and right.is_symbol()

    elif lit.is_function_application() and lit.get_type() == BOOL:
        return all(arg.is_symbol() for arg in lit.args())

    elif lit.is_not() and lit.args()[0].is_function_application() and lit.args()[0].get_type() == BOOL:
        return all(arg.is_symbol() for arg in lit.args()[0].args())
    return False


# check if `cube` is a flat cube
def is_flat_cube(cube):
  if not is_cube(cube):
    return False
  for lit in cube:
    if not is_flat_lit(lit):
      return False
  return True

def flattening(formula):
    cube = list(formula.args()) if formula.is_and() else [formula]
    new_cube = []
    step = 0

    while cube != new_cube:
        new_cube = cube.copy()
        step += 1
        print("")
        print("**********************************************")
        print("step: ", step)
        print("cube: ", cube)

        cube = equal_rule(cube)
        if cube != new_cube:
            print("equal_rule")
            continue

        cube = not_s_rule(cube)
        if cube != new_cube:
            print("not_s_rule")
            continue

        cube = not_t_rule(cube)
        if cube != new_cube:
            print("not_t_rule")
            continue

        cube = function_rule(cube)
        if cube != new_cube:
            print("function_rule")
            continue

        cube = predicat_rule(cube)
        if cube != new_cube:
            print("predicat_rule")
            continue

        cube = not_predicat_rule(cube)
        if cube != new_cube:
            print("not_predicat_rule")
            continue
        return And(cube)


def equal_rule(cube):
    for lit in cube:
        if lit.is_equals():
            left, right = lit.args()
            if not left.is_symbol():
                cube.remove(lit)
                new_symbol = Symbol(f"x_{left}", left.get_type())
                cube.extend([EqualsOrIff(new_symbol, right), EqualsOrIff(new_symbol, left)])
                return cube
    return cube

def not_s_rule(cube):
    for lit in cube:
        if lit.is_not() and lit.args()[0].is_equals():
            left, right = lit.args()[0].args()
            if not left.is_symbol():
                cube.remove(lit)
                new_symbol = Symbol(f"x_{left}", left.get_type())
                cube.extend([Not(EqualsOrIff(new_symbol, right)), EqualsOrIff(new_symbol, left)])
                return cube
    return cube

def not_t_rule(cube):
    for lit in cube:
        if lit.is_not() and lit.args()[0].is_equals():
            left, right = lit.args()[0].args()
            if left.is_symbol() and not right.is_symbol():
                cube.remove(lit)
                new_symbol = Symbol(f"x_{right}", right.get_type())
                cube.extend([Not(EqualsOrIff(left, new_symbol)), EqualsOrIff(new_symbol, right)])
                return cube
    return cube

def function_rule(cube):
    for lit in cube:
        if lit.is_equals():
            left, right = lit.args()
            if left.is_symbol() and right.is_function_application():
                non_symbol = next((arg for arg in right.args() if not arg.is_symbol()), [])
                if non_symbol != []:
                    cube.remove(lit)
                    new_symbol = Symbol(f"x_{non_symbol}", non_symbol.get_type())
                    new_args = [new_symbol if arg == non_symbol else arg for arg in right.args()]
                    new_func = Function(right.function_name(), new_args)
                    cube.extend([EqualsOrIff(left, new_func), EqualsOrIff(new_symbol, non_symbol)])
                    return cube
    return cube

def predicat_rule(cube):
    for lit in cube:
        if lit.is_function_application() and lit.get_type() == BOOL:
            non_symbol = next((arg for arg in lit.args() if not arg.is_symbol()), [])
            if non_symbol != []:
                cube.remove(lit)
                new_symbol = Symbol(f"x_{non_symbol}", non_symbol.get_type())
                new_args = [new_symbol if arg == non_symbol else arg for arg in lit.args()]
                new_predicat = Function(lit.function_name(), new_args)
                cube.extend([new_predicat, EqualsOrIff(new_symbol, non_symbol)])
                return cube
    return cube

def not_predicat_rule(cube):
    for lit in cube:
        if lit.is_not() and lit.args()[0].is_function_application() and lit.args()[0].get_type() == BOOL:
            non_symbol = next((arg for arg in lit.args()[0].args() if not arg.is_symbol()), [])
            if non_symbol != []:
                cube.remove(lit)
                new_symbol = Symbol(f"x_{non_symbol}", non_symbol.get_type())
                new_args = [new_symbol if arg == non_symbol else arg for arg in lit.args()[0].args()]
                new_predicat = Function(lit.args()[0].function_name(), new_args)
                cube.extend([Not(new_predicat), EqualsOrIff(new_symbol, non_symbol)])
                return cube
    return cube






# read path from input
path = sys.argv[1]
with open(path, "r") as f:
    smtlib = f.read()

    print("smtlib: ", smtlib)
    # parse the smtlib file and get a formula
    parser = SmtLibParser()
    script = parser.get_script(cStringIO(smtlib))
    # print("script: ", script)
    formula = script.get_last_formula()
    print("")
    print("formula: ", formula)
    is_single_clause = len(formula.args()) == 1 if formula.is_and() else True


    # we are assuming `formula` is a flat cube.
    # `cube` represents `formula` as a list of literals
    cube = []
    if is_single_clause:
        cube = [formula]
    else:
        cube = formula.args()
    print("")
    print("cube: ", cube)
    print("is_cube: ", is_cube(cube))
    print("is_flat_cube: ", is_flat_cube(cube))
    if not is_flat_cube(cube):
        flat_cube = flattening(formula)
        print()
        print("flattern: ", flat_cube)
        print("is_flat_cube: ", is_flat_cube(flat_cube.args()))








