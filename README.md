# Automated Reasoning Course

Course materials for an Automated Reasoning course, including solver implementations and interactive browser-based labs.

---

## Interactive Labs

Step-by-step algorithm visualizations — open `index.html` in a browser to start.

| Lab | Topic |
|---|---|
| [Horn Clause Solver](horn/index.html) | Linear-time SAT for Horn CNF via unit propagation |
| [Tseytin Transformation](tseytin/index.html) | Convert propositional formula to equisatisfiable CNF |
| [DPLL](dpll/index.html) | Davis–Putnam–Logemann–Loveland backtracking SAT solver |
| [Basic CDCL](basic-cdcl/index.html) | Conflict-Driven Clause Learning without backjumping |
| [CDCL](cdcl/index.html) | Full CDCL with UIP analysis and non-chronological backjumping |
| [Term Flattening](flatten/index.html) | EUF pre-processing — flatten a cube one rule at a time |
| [Congruence Closure](cc/index.html) | EUF theory solver using equivalence classes |
| [Union-Find](uf/index.html) | Union-Find with path compression and union by rank |
| [DPLL(T)](dpll-t/index.html) | DPLL modulo theories — SAT solver + theory solver cooperation |
| [Integer Difference Logic](idl/index.html) | QF_IDL satisfiability via constraint graph and Bellman-Ford |
| [Ackermanization](ackermann/index.html) | Reduce QF_UF to QF_EQ by replacing function apps with constants |
| [Bit Blasting](bitblasting/index.html) | Reduce QF_BV to propositional logic — one Boolean variable per bit |
| [Prenex Normal Form](pnf/index.html) | Convert first-order formulas to PNF in four steps |

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
