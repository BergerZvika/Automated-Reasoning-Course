# Automated Reasoning Course

Course materials for an Automated Reasoning course, including solver implementations and interactive browser-based labs.

---

## Interactive Labs

Step-by-step algorithm visualizations — open `labs/index.html` in a browser to start.

| Lab | Topic | Lecture |
|---|---|---|
| [Horn Clause Solver](labs/horn/index.html) | Linear-time SAT for Horn CNF via unit propagation | 2 |
| [DPLL](labs/dpll/index.html) | Davis–Putnam–Logemann–Loveland backtracking SAT solver | 4 |
| [Basic CDCL](labs/basic-cdcl/index.html) | Conflict-Driven Clause Learning without backjumping | 5 |
| [CDCL](labs/cdcl/index.html) | Full CDCL with UIP analysis and non-chronological backjumping | 5 |
| [Tseytin Transformation](labs/tseytin/index.html) | Convert propositional formula to equisatisfiable CNF | 7 |
| [Term Flattening](labs/flatten/index.html) | EUF pre-processing — flatten a cube one rule at a time | 7 |
| [Congruence Closure](labs/cc/index.html) | EUF theory solver using equivalence classes | 8 |
| [Union-Find](labs/uf/index.html) | Union-Find with path compression and union by rank | 9 |
| [DPLL(T)](labs/dpllt/index.html) | DPLL modulo theories — SAT solver + theory solver cooperation | 9 |
| [Ackermanization](labs/ackermann/index.html) | Reduce QF_UF to QF_EQ by replacing function apps with constants | — |
| [Bit Blasting](labs/bitblasting/index.html) | Reduce QF_BV to propositional logic — one Boolean variable per bit | 10–11 |
| [Prenex Normal Form](labs/pnf/index.html) | Convert first-order formulas to PNF in four steps | 13 |

---

## Solver Implementations

### Horn Clause Solver — `horn-solver/`
Linear-time satisfiability solver for Horn CNF formulas. Includes a debug variant and a benchmark generator.

- `horn-solver.py` — main solver
- `horn-solver-debug.py` — verbose step-by-step output
- `naive-solver.py` — brute-force baseline
- `generate_horn_cnf.py` — benchmark generator
- `horn_cnf_benchmarks/` — benchmark instances

### DPLL / CDCL Solvers — `cdcl-solver/`
SAT solvers from basic DPLL up to full CDCL with conflict analysis.

- `dpll-solver.py` — DPLL
- `basic-cdcl-solver.py` — Basic CDCL
- `cdcl-solver.py` — CDCL with non-chronological backjumping
- `*-debug.py` — verbose variants
- `benchmarks/` — CNF benchmark instances

### DPLL(T) — `dpll-t/`
DPLL modulo theories combining a SAT solver with a theory solver (Congruence Closure / Union-Find).

- `dpll_solver.py` — DPLL core
- `cc_solver.py` — Congruence Closure theory solver
- `dpllt-solver.py` — DPLL(T) integration
- `tseytin.py` — Tseytin transformation
- `tr.py` — term rewriting utilities
- `*-debug.py` — verbose variants
- `benchmarks/` — benchmark instances

### CC / UF Solvers — `cc-solver/`, `uf-flattern/`
Theory solvers for Equality with Uninterpreted Functions (EUF).

- `cc-solver/cc-solver.py` — Congruence Closure solver
- `uf-flattern/flattern.py` — Union-Find with term flattening
- `*-debug.py` — verbose variants
- `benchmarks/` — benchmark instances

### Ackermanization — `ackermanization/`
Reduction from QF_UF to QF_EQ by replacing function applications with fresh constants and adding congruence axioms.

- `ackermannization.py` — Python implementation
- `ackerman.html` — standalone interactive demo

### pySMT Examples — `pysmt/`
Example scripts using the [pySMT](https://github.com/pysmt/pysmt) library.

- `pysmt-hello_world.py` — getting started
- `pysmt-basic.py` — basic formula construction
- `pysmt-lia.py` — Linear Integer Arithmetic
- `pysmt_portfolio.py` — portfolio solving
- `quantifiers.py` — quantified formulas
