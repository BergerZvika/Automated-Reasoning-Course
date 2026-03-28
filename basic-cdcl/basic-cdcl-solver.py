# importing system module for reading files
import sys
import itertools

SAT = "sat"
UNSAT = "unsat"
COMMENT = "c"
PROBLEM = "p"
END = "0"

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

# input cnf: a formula
# input n_vars: the number of variables in the formula
# input n_clauses: the number of clauses in the formula
# output: True if cnf is satisfiable, False otherwise
def cdcl_solve(cnf, n_vars, n_clauses):
    m, f, d, k = [], cnf, [], "no"
    pre_m, pre_f, pre_d, pre_k = [], [], [], "no"
    print("f: ", f)

    while (pre_m, pre_f, pre_d, pre_k) != (m, f, d, k):
        pre_m = m.copy() if m is not None else None
        pre_f = f.copy() if f is not None else None
        pre_d = d.copy() if d is not None else None
        pre_k = k.copy() if k !="no" else "no"

        m, f, d, k = conflict(m, f, d, k)
        if (pre_m, pre_f, pre_d, pre_k) != (m, f, d, k):
            continue

        m, f, d, k = explain(m, f, d, k)
        if (pre_m, pre_f, pre_d, pre_k) != (m, f, d, k):
                continue

        m, f, d, k = backjump(m, f, d, k)
        if (pre_m, pre_f, pre_d, pre_k) != (m, f, d, k):
            continue

        m, f, d, k = unit_propagate(m, f, d, k)
        if (pre_m, pre_f, pre_d, pre_k) != (m, f, d, k):
            continue

        m, f, d, k = decide(m, f, d, k)
        if (pre_m, pre_f, pre_d, pre_k) != (m, f, d, k):
            continue

        m, f, d, k = fail(m, f, d, k)
        if (pre_m, pre_f, pre_d, pre_k) != (m, f, d, k):
            break

    return not (f is None and m is None and d is None)

def conflict(m, f, d, k):
    if k != "no":
        return m, f, d, k
    for clause in f:
        if all(-lit in m for lit in clause):
            return m, f, d, clause
    return m, f, d, k

def explain(m, f, d, k):
    if k == "no":
        return m, f, d, k
    for lit in k:
        if -lit in m:
            for clause in [c for c in f if -lit in c]:
                c = [l for l in clause if l != -lit]
                conflict = model_conflict(m[:m.index(-lit) -1], [c])
                if conflict:
                    new_k = [l for l in list(set(k + c)) if l != lit]
                    return m, f, d, new_k
    return m, f, d, k

def backjump(m, f, d, k):
    if k == "no":
        return m, f, d, k
    for l in k:
        for l0 in d:
            l0n = m[m.index(l0):]
            if all(-lit in m[:m.index(l0)-1] for lit in k if lit != l) and -l in l0n:
                return m[:m.index(l0)-1] + [l], f, [lit for lit in d if lit not in l0n], "no"
    return m, f, d, k

def unit_propagate(m, f, d, k):
    for clause in f:
        for lit in clause:
            if lit not in m and -lit not in m and lit != 0:
                conflict = model_conflict(m, [[l for l in clause if l != lit]])
                if conflict:
                    m += [lit]
                    return m, f, d, k
    return m, f, d, k


def decide(m, f, d, k):
    l = choose_lit(m, f)

    if l is None:
        return m, f, d, k

    d += [l]
    m += [l]
    return m, f, d, k


def choose_lit(m, f):
    for c in f:
        for l in c:
            if l not in m and -l not in m:
                return l
    return None


def fail(m, f, d, k):
    # if len(d) == 0 and model_conflict(m, f):
    if len(d) == 0 and k != "no":
        return None, None, None, None
    return m, f, d, k

# input m: a model
# input f: a formula
# output: True if model m is satisfy negation of clause in f.
def model_conflict(m, f):
    return any(all(-lit in m for lit in clause) for clause in f)


######################################################################

# get path to cnf file from the command line
path = sys.argv[1]

# parse the file
cnf, num_vars, num_clauses = parse_dimacs_path(path)

# check satisfiability based on the chosen algorithm
# and print the result
print(SAT if cdcl_solve(cnf, num_vars, num_clauses) else UNSAT)
