import random


def generate_horn_clause(n_vars):
    """
    Generate a random Horn clause with at most one positive literal.
    :param n_vars: The number of variables.
    :return: A list representing the clause.
    """
    clause = []
    positive_literal_added = False

    # Randomly decide how many literals the clause should have
    clause_size = random.randint(1, 3)  # Let's limit to 1-3 literals per clause

    for _ in range(clause_size):
        literal = random.randint(1, n_vars)
        if not positive_literal_added and random.random() < 0.5:
            # Add a positive literal with 50% chance
            clause.append(literal)
            positive_literal_added = True
        else:
            # Add a negative literal
            clause.append(-literal)

    return clause


def generate_horn_cnf(n_vars, n_clauses):
    """
    Generate a random Horn CNF formula.
    :param n_vars: The number of variables.
    :param n_clauses: The number of clauses.
    :return: A list of Horn clauses.
    """
    cnf = []
    for _ in range(n_clauses):
        clause = generate_horn_clause(n_vars)
        cnf.append(clause)
    return cnf


def save_dimacs(path, cnf, n_vars, n_clauses):
    """
    Save the CNF formula in DIMACS format.
    :param path: Path to save the file.
    :param cnf: The CNF formula (list of clauses).
    :param n_vars: Number of variables.
    :param n_clauses: Number of clauses.
    """
    with open(path, 'w') as f:
        f.write(f"p cnf {n_vars} {n_clauses}\n")
        for clause in cnf:
            clause_str = " ".join(map(str, clause)) + " 0\n"
            f.write(clause_str)


def generate_horn_cnf_files(num_files=10, n_vars=5, n_clauses=5, folder="horn_cnf_benchmarks"):
    """
    Generate multiple Horn CNF files and save them.
    :param num_files: Number of files to generate.
    :param n_vars: Number of variables for each CNF formula.
    :param n_clauses: Number of clauses for each CNF formula.
    :param folder: Folder to save the files in.
    """
    import os
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i in range(1, num_files + 1):
        cnf = generate_horn_cnf(n_vars, n_clauses)
        file_path = os.path.join(folder, f"horn_cnf_{i + 20}.cnf")
        save_dimacs(file_path, cnf, n_vars, n_clauses)
        print(f"Generated {file_path}")


# Generate 10 Horn CNF files with 5 variables and 5 clauses each
generate_horn_cnf_files(num_files=20, n_vars=4, n_clauses=8)
