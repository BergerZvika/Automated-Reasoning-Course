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
                cnf.append(clause)
    return cnf, num_vars, num_clauses

# input cnf: a horn formula
# input n_vars: the number of variables in the formula
# input n_clauses: the number of clauses in the formula
# output: True if cnf is satisfiable, False otherwise
def horn_solver(cnf, n_vars, n_clauses):
    print("cnf:")
    print(cnf)

    while True:
        # Step 1: Find a clause with a positive literal
        chosen_lit = next((lit for clause in cnf for lit in clause if lit > 0 and len(clause) == 1), None)
        print()
        print("chosen_lit: ", chosen_lit)
        if chosen_lit is None:
            break

         # Step 2: Remove all clauses that contain this positive literal
        cnf = [c for c in cnf if chosen_lit not in c]
        print("Remove all clauses that contain this positive literal:")
        print(cnf)

        # Step 3: Remove the corresponding negative literal from all other clauses
        cnf = [[lit for lit in clause if lit != -chosen_lit] for clause in cnf]
        print("Remove the corresponding negative literal from all other clauses:")
        print(cnf)

        # Step 4: Check if any clause becomes empty
        if any(len(clause) == 0 for clause in cnf):
            return False  # Unsatisfiable (we found an empty clause)

    # Step 5: If no more positive literals, return True (satisfiable)
    return True


######################################################################

# get path to cnf file from the command line
path = sys.argv[1]

# parse the file
cnf, num_vars, num_clauses = parse_dimacs_path(path)

# check satisfiability based on the horn algorithm
# and print the result
print(SAT if horn_solver(cnf, num_vars, num_clauses) else UNSAT)

