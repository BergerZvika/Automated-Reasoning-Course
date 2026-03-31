"""
idl-solver.py  —  Decision procedure for Integer Difference Logic (IDL)
                  using Bellman-Ford negative-cycle detection.

Usage:
    python idl-solver.py constraints.txt

Constraint file format (one per line):
    x - y <= 5
    y - x <= -5
    ...

Algorithm:
    1. Build a directed weighted graph: constraint "x - y <= c" → edge x→y weight c
    2. Initialise all distances to 0
    3. Run n rounds of Bellman-Ford edge relaxation (n = number of variables)
    4. If any edge can still be relaxed after round n → NEGATIVE CYCLE → UNSAT
    5. Otherwise SAT; the final distances give a satisfying model
"""
import sys, re
from collections import defaultdict

# ── PARSER ────────────────────────────────────────────────────────────────────
def parse_constraints(text):
    edges = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        m = re.match(r'([A-Za-z_]\w*)\s*-\s*([A-Za-z_]\w*)\s*(<=|<|>=|>|=)\s*(-?\d+)', line)
        if not m:
            raise ValueError(f"Cannot parse: {line!r}")
        lv, rv, op, cs = m.groups()
        c = int(cs)
        if op == '<=':
            edges.append((lv, rv, c))
        elif op == '<':
            edges.append((lv, rv, c - 1))
        elif op == '>=':
            edges.append((rv, lv, -c))
        elif op == '>':
            edges.append((rv, lv, -c - 1))
        elif op == '=':
            edges.append((lv, rv, c))
            edges.append((rv, lv, -c))
    return edges

# ── BELLMAN-FORD ──────────────────────────────────────────────────────────────
def solve(edges):
    # Collect variables
    vars_ = sorted({v for e in edges for v in (e[0], e[1])})
    n = len(vars_)

    dist = {v: 0 for v in vars_}
    pred = {v: None for v in vars_}

    print(f"Variables: {', '.join(vars_)}")
    print(f"Edges: {len(edges)}")
    print(f"Initial distances: {dist}")
    print()

    # Bellman-Ford: n rounds
    for rnd in range(1, n + 2):  # +1 extra round for cycle detection
        updated = []
        for (u, v, w) in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated.append((u, v, w, dist[v]))

        if rnd <= n:
            print(f"Round {rnd}: {len(updated)} update(s)")
            for u, v, w, nd in updated:
                print(f"  d[{v}] = d[{u}] + {w} = {nd}")
            if not updated:
                print(f"  → No changes, early SAT")
                break
        else:
            # Extra round — check for negative cycle
            if updated:
                print(f"\nRound {n+1} (extra): still {len(updated)} update(s) → NEGATIVE CYCLE")
                # Trace cycle
                v = updated[0][1]
                for _ in range(n):
                    v = pred[v] or v
                cycle = [v]
                cur = pred[v]
                visited = {v}
                while cur and cur != v and cur not in visited:
                    cycle.insert(0, cur)
                    visited.add(cur)
                    cur = pred[cur]
                cycle.insert(0, v)
                weight = sum(
                    w for (u, vv, w) in edges
                    if any(cycle[i]==u and cycle[i+1]==vv for i in range(len(cycle)-1))
                )
                path = ' → '.join(cycle)
                print(f"Negative cycle: {path}  (weight = {weight})")
                print("\nResult: UNSAT")
                return False, dist, cycle
            else:
                break

    print(f"\nDistances: {dist}")
    print("Result: SAT")
    return True, dist, []

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        print("Running built-in slide example (UNSAT)...")
        text = """
x - y <= 5
y - x <= -5
y - z <= -2
x - z <= -3
w - x <= 2
x - w <= -2
z - w <= -1
"""
    else:
        with open(sys.argv[1]) as f:
            text = f.read()

    try:
        edges = parse_constraints(text)
        sat, dist, cycle = solve(edges)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
