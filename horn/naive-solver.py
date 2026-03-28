# importing system module for reading files
import sys
import itertools

SAT = "sat"
UNSAT = "unsat"


# input path:  a path to a cnf file
# output: the formula represented by the file,
#         the number of variables,
#         and the number of clauses
def parse_dimacs_path(path):
    cnf = []
    num_vars = 0
    num_clauses = 0
    with open(path, 'r') as file:
        for line in file:
            if line.startswith('c'):
                continue
            literals = line.split()
            if line.startswith('p cnf'):
                num_vars = int(literals[2])
                num_clauses = int(literals[3])
                continue
            clause = [int(lit) for lit in literals if lit != '0']
            if len(clause) > 0:
                cnf.append(clause )
    return cnf, num_vars, num_clauses


def satisfies_clause(clause, assignment):
    for literal in clause:
        var = abs(literal) - 1  # Variables are 1-indexed, assignments are 0-indexed
        value = assignment[var]
        if literal < 0:  # If the literal is negative, take the negation of the assignment value
            value = not value
        if value:  # If the literal is satisfied, the clause is satisfied
            return True
    return False


def satisfies_all_clauses(cnf, assignment):
    for clause in cnf:
        if not satisfies_clause(clause, assignment):
            return False
    return True

# input cnf: a formula
# input n_vars: the number of variables in the formula
# input n_clauses: the number of clauses in the formula
# output: True if cnf is satisfiable, False otherwise
def naive_solver(cnf, n_vars, n_clauses):
    if n_clauses == 0:
        return True
    for assignment in itertools.product([True, False], repeat=n_vars):
        if satisfies_all_clauses(cnf, assignment):
            return True
    return False


######################################################################

# get path to cnf file from the command line
path = sys.argv[1]

# parse the file
cnf, num_vars, num_clauses = parse_dimacs_path(path)

# check satisfiability based on the naive algorithm
# and print the result
print(SAT if naive_solver(cnf, num_vars, num_clauses) else UNSAT)

