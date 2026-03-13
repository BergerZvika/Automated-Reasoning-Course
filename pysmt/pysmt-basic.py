from pysmt.shortcuts import Solver, And, Or, Not, BOOL, Symbol, TRUE

solver = Solver(name="z3")

a = Symbol("a", BOOL)
b = Symbol("b", BOOL)

v = []
for i in range(0, 5):
    v += [ Symbol("x" + str(i), BOOL) ]

solver.add_assertion(And(a, b))
# solver.add_assertion(Not(And(a, b)))
solver.add_assertion(Or(v))
r = solver.check_sat()
print("result: ", r)
print("********************************")
print("model values:")
for var in v:
    val = solver.get_value(var)
    print(var, ":", val)
print("********************************")

a_val = solver.get_value(a)
print("a_val:", a_val)
print("type of a_val:", type(a_val))
print("********************************")

# a_val is not a Boolean
print(a_val == True)

# a_val is a pysmt object
print(a_val == TRUE())
print(a_val.is_true())
