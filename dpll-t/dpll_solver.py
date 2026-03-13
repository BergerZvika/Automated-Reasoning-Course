# importing system module for reading files
import sys
import itertools

SAT = "sat"
UNSAT = "unsat"
COMMENT = "c"
PROBLEM = "p"
END = "0"

# in what follows, a *formula* is a collection of clauses,
# a clause is a collection of literals,
# and a literal is a non-zero integer.

# input path:  a path to a cnf file
# output: the formula represented by the file,
#         the number of variables,
#         and the number of clauses
def parse_dimacs_path(path):
    count = 0
    lines = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            literals = line.split()
            first_char = line[0]
            if first_char == PROBLEM:
                num_vars = int(literals[2])
                num_clauses = int(literals[3])
                continue
            if first_char == COMMENT:
                continue
            count += 1
            integer_line = [int(lit) for lit in literals if lit != END]
            lines.append(integer_line)
    return lines, num_vars, num_clauses

def evaluate(cnf, v):
    for clause in cnf:
        is_sat = False
        for lit in clause:
            var = abs(lit)
            if v[var - 1] and lit > 0:
                is_sat = True
            elif not v[var - 1] and lit < 0:
                is_sat = True
        if not is_sat:
            return False
    return True


# input cnf: a formula
# input n_vars: the number of variables in the formula
# input n_clauses: the number of clauses in the formula
# output: True if cnf is satisfiable, False otherwise
def sat_solver(cnf):
    m, f, d = [], cnf, []
    pre_m, pre_f, pre_d = [], [], []

    while (pre_m, pre_f, pre_d) != (m, f, d):
        pre_m = m.copy() if m is not None else None
        pre_f = f.copy() if f is not None else None
        pre_d = d.copy() if d is not None else None

        m, f, d = unit_propagate(m, f, d)
        if (pre_m, pre_f, pre_d) != (m, f, d):
            continue

        m, f, d = backtrack(m, f, d)
        if (pre_m, pre_f, pre_d) != (m, f, d):
            continue

        m, f, d = decide(m, f, d)
        if (pre_m, pre_f, pre_d) != (m, f, d):
            continue

        m, f, d = fail(m, f, d)
        if (pre_m, pre_f, pre_d) != (m, f, d):
            break

    return m


def unit_propagate(m, f, d):
    if m is None and f is None and d is None:
        return m, f, d

    for clause in f:
        for lit in clause:
            if lit not in m and -lit not in m and lit != 0:
                conflict = model_conflict(m, [[l for l in clause if l != lit]])
                if conflict:
                    m += [lit]
                    return m, f, d
    return m, f, d


def decide(m, f, d):
    if m == None and f == None and d == None:
        return m, f, d

    l = choose_lit(m, f)

    if l is None:
        return m, f, d

    d += [l]
    m += [l]
    return m, f, d


def choose_lit(m, f):
    for c in f:
        for l in c:
            if l not in m and -l not in m:
                return l
    return None


def fail(m, f, d):
    if m is None and f is None and d is None:
        return m, f, d

    if len(d) == 0 and model_conflict(m, f):
        return None, None, None
    return m, f, d

# input m: a model
# input f: a formula
# output: True if model m is satisfy f.
def model_evaluation(m, f):
    for clause in f:
        is_sat = False
        for lit in clause:
            if lit in m:
                is_sat = True
                break
        if not is_sat:
            return False
    return True

# input m: a model
# input f: a formula
# output: True if model m is satisfy negation of clause in f.
def model_conflict(m, f):
    for clause in f:
        conflict = True
        for lit in clause:
            if -lit not in m:
                conflict = False
                break
        if conflict:
            return True
    return False


def backtrack(m, f, d):
    if m is None and f is None and d is None:
        return m, f, d

    conflict = model_conflict(m, f)
    if conflict and len(d) > 0:
        lit = d[-1]
        d.remove(lit)
        flag = False
        while len(m) > 0 and m[-1] != lit:
            m.remove(m[-1])
        m.remove(lit)
        m += [-lit]
    return m, f, d