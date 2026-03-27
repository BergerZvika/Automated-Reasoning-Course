# DPLL Interactive Tutorial

An interactive, step-by-step visualization of the **Davis–Putnam–Logemann–Loveland (DPLL)** algorithm for propositional satisfiability.
Based on the solver from **Class 4** of the Automated Reasoning course.

---

## How to Run

```bash
# Option 1: just open the file in your browser
firefox index.html
xdg-open index.html   # Linux
open index.html       # macOS

# Option 2: serve locally (avoids any file:// restrictions)
python3 -m http.server 8080
# then visit http://localhost:8080
```

No dependencies, no build step — it's a single HTML file.

---

## What is DPLL?

DPLL is a complete, backtracking-based search algorithm for deciding the satisfiability of propositional logic formulas in **Conjunctive Normal Form (CNF)**.

A CNF formula is a conjunction (AND) of **clauses**, each clause being a disjunction (OR) of **literals** (a variable or its negation).

**State** `(M, F, D)`:
| Symbol | Meaning |
|--------|---------|
| `M` | **Assignment trail** — ordered list of assigned literals |
| `F` | **Formula** — the set of clauses (never changes) |
| `D` | **Decision set** — subset of M that were *freely decided* |

A literal `l` in M means its variable is **TRUE**; `-l` means **FALSE**.

---

## The Four DPLL Rules

### 1. Unit Propagate
```
M, F  ⊢  M·l, F
```
**Precondition:** There exists a clause `C ∈ F` such that:
- All literals in `C` except `l` are **false** in M (their negations appear in M)
- `l` is **unassigned**

**Effect:** Add `l` to M (forced — no choice).

**Why:** If all other literals in a clause are false, the last remaining literal *must* be true to satisfy the clause.

---

### 2. Decide
```
M, F, D  ⊢  M·l, F, D·l
```
**Precondition:** Some literal `l` is unassigned and there is no conflict in `(M, F)`.

**Effect:** Add `l` to both M and D (marks it as a decision point).

**Why:** When no unit clause exists, we make a *free choice*. The chosen literal is recorded in D so we can backtrack to it later if needed.

---

### 3. Backtrack
```
M·l^D·M', F, D·l  ⊢  M·¬l, F, D
```
**Precondition:** There is a **conflict** (some clause is fully false in M) **and** D ≠ ∅.

**Effect:**
1. Find the last decision literal `l` in D
2. Remove from M everything from `l` onwards (i.e., `l` and all propagations after it)
3. Remove `l` from D
4. Add `¬l` to M (as a forced assignment, not a new decision)

**Why:** The decision `l` led to a contradiction. We flip it and try `¬l` instead.

---

### 4. Fail (UNSAT)
```
M, F, ∅  ⊢  UNSAT
```
**Precondition:** There is a **conflict** in `(M, F)` **and** D = ∅ (no decisions left).

**Effect:** Return **UNSATISFIABLE**.

**Why:** We have exhausted all possible decisions. The formula cannot be satisfied.

---

## Satisfiability (SAT Terminal)

After any assignment step, if **all clauses** have at least one **true** literal in M, the formula is **satisfiable**. The current M gives a satisfying assignment.

---

## Formula Input Syntax

| Construct | Syntax |
|-----------|--------|
| Variable | Any alphanumeric word: `x1`, `p`, `alpha` |
| Negation | `-x1`, `¬x1`, `!x1` |
| OR (within clause) | `\|`, `∨`, `OR` |
| AND (between clauses) | `,`, `&`, `;`, newline |

**Examples:**
```
x1 | x2 | -x3, -x1 | x2, -x2 | -x3
p | q, -p | r, -q | -r
x1 & -x1            (UNSAT)
-x1 | -x2, x2 | x3, x1    (chain propagation)
```

---

## Using the Tutorial

1. **Load** a formula (or pick an example)
2. **Read the hint** — it tells you which actions are applicable and why
3. **Click an action button** (only applicable actions are enabled)
   - **Unit Propagate**: forces the unit literal (no choice)
   - **Decide**: opens a modal — pick any unassigned variable and a value
   - **Backtrack**: flips the last decision and rolls back
   - **Fail**: concludes UNSAT (only when no decisions remain)
4. **Read the explanation** — shows the exact rule applied and which clause triggered it
5. **Undo** any step with the ← button
6. **Auto-Solve** to watch the algorithm run automatically (priority: Unit → Backtrack → Decide → Fail)

---

## Example Walkthrough: `x1 | x2, -x1 | x2, x1 | -x2, -x1 | -x2`

| Step | Action | M | D | Notes |
|------|--------|---|---|-------|
| 0 | — | ∅ | ∅ | Initial |
| 1 | Decide x1=T | {x1} | {x1} | Free choice |
| 2 | Unit Prop → x2 | {x1, x2} | {x1} | C2 is unit: `(-x1 ∨ x2)` with x1=T |
| 3 | Conflict | {x1, x2} | {x1} | C4 `(-x1 ∨ -x2)` is fully false |
| 4 | Backtrack | {-x1} | ∅ | Flip x1, remove x2 |
| 5 | Unit Prop → -x2 | {-x1, -x2} | ∅ | C3 is unit: `(x1 ∨ -x2)` with x1=F |
| 6 | Conflict | — | — | C1 `(x1 ∨ x2)` is fully false |
| 7 | Fail | — | ∅ | D=∅, no decisions → UNSAT |

---

## Connection to Class 4 Code

This tutorial directly implements the inference rules from `class-4/dpll-solver.py`:

```python
# Priority order in the main loop:
unit_propagate(m, f, d)   →  Unit Propagate button
backtrack(m, f, d)        →  Backtrack button
decide(m, f, d)           →  Decide button
fail(m, f, d)             →  Fail button
```

The state `(m, f, d)` in Python maps to `(M, F, D)` in the tutorial.
