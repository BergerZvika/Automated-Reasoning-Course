from pysmt.shortcuts import Symbol, And, Or, Not, ExactlyOne, Solver
from pysmt.typing import BOOL
import random


def generate_random_hc_graph(n, extra=8):
    nodes = list(range(1, n + 1))
    perm = nodes[:]
    random.shuffle(perm)
    # Guarantee a Hamiltonian cycle exists
    edges = set()
    for i in range(n):
        a, b = perm[i], perm[(i + 1) % n]
        edges.add((min(a, b), max(a, b)))
    # Add random extra edges
    attempts = 0
    while len(edges) < n + extra and attempts < 300:
        a, b = random.sample(nodes, 2)
        edges.add((min(a, b), max(a, b)))
        attempts += 1
    return nodes, list(edges)


def hamiltonian_cycle_sat(nodes, edges):
    n = len(nodes)
    edge_set = set(edges) | {(b, a) for a, b in edges}
    pos = {(v, i): Symbol(f"pos_{v}_{i}", BOOL) for v in nodes for i in range(n)}

    constraints = []

    # Each vertex appears at exactly one position
    for v in nodes:
        constraints.append(ExactlyOne([pos[(v, i)] for i in range(n)]))

    # Each position has exactly one vertex
    for i in range(n):
        constraints.append(ExactlyOne([pos[(v, i)] for v in nodes]))

    # Consecutive positions must be connected by an edge
    for i in range(n):
        j = (i + 1) % n
        for v in nodes:
            for u in nodes:
                if v != u and (v, u) not in edge_set:
                    constraints.append(Or(Not(pos[(v, i)]), Not(pos[(u, j)])))

    with Solver(name="z3") as solver:
        solver.add_assertion(And(constraints))
        if solver.solve():
            cycle = [None] * n
            for v in nodes:
                for i in range(n):
                    if solver.get_value(pos[(v, i)]).is_true():
                        cycle[i] = v
            return cycle
        return None


n = 10
nodes, edges = generate_random_hc_graph(n, extra=8)

cycle = hamiltonian_cycle_sat(nodes, edges)
if cycle:
    cycle_edges = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]
    print("HAMILTON_CYCLE_RESULT")
    print(f"N={len(nodes)}")
    for v in nodes:
        print(f"V {v}")
    for a, b in edges:
        print(f"E {a} {b}")
    for a, b in cycle_edges:
        print(f"C {a} {b}")
    print("---")
    path = " -> ".join(str(v) for v in cycle) + f" -> {cycle[0]}"
    print(f"Hamiltonian cycle found: {path}")
else:
    print("No Hamiltonian cycle exists.")
