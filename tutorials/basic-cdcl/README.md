# CDCL Interactive Tutorial

An interactive, step-by-step visualization of the **Conflict-Driven Clause Learning (CDCL)** algorithm.
Based on the solvers in **Class 4** (`cdcl-solver.py`, `basic-cdcl-solver.py`).

---

## How to Run

```bash
firefox index.html
xdg-open index.html   # Linux
open index.html       # macOS
# or serve locally:
python3 -m http.server 8080  → http://localhost:8080
```

No build step — single HTML file.

---

## CDCL vs DPLL

| Feature | DPLL | CDCL |
|---------|------|------|
| Backtracking | Chronological (flip last decision) | **Non-chronological** (jump to assertion level) |
| Conflict analysis | None | Resolution until 1-UIP |
| Clause learning | No | **Yes — adds learned clause to F** |
| Conflict clause K | No | **Yes — K is tracked and resolved** |

---

## State `(M, F, D, K)`

| Symbol | Meaning |
|--------|---------|
| `M` | **Assignment trail** — ordered list of assigned literals |
| `F` | **Formula** — original + learned clauses |
| `D` | **Decision set** — subset of M that were freely decided |
| `K` | **Conflict clause** — the clause being analyzed (`null` = no conflict) |

---

## The Seven CDCL Rules

### 1. Unit Propagate
```
M, F, D, ∅  ⊢  M·l, F, D, ∅
```
**When:** K = ∅, ∃ clause C ∈ F with one unassigned literal `l` (all others false in M).
**Effect:** Add `l` to M (forced). Same as in DPLL.

---

### 2. Decide
```
M, F, D, ∅  ⊢  M·l, F, D·l, ∅
```
**When:** K = ∅, no conflict, some variable unassigned.
**Effect:** Freely assign `l`, add to both M and D (marks a potential backjump point).

---

### 3. Conflict
```
M, F, D, ∅  ⊢  M, F, D, K
```
**When:** K = ∅, some clause C ∈ F has ALL literals false in M.
**Effect:** Set K = C (begin conflict analysis).

---

### 4. Explain (Resolution Step)
```
M, F, D, K  ⊢  M, F, D, K'
```
**When:** K ≠ ∅, ∃ literal `l ∈ K` such that `¬l ∈ M` was forced by a unit clause `C'`.
**Effect:** Resolve K with C' (the reason clause for `¬l`) on variable `|l|`:

```
K' = (K ∖ {l}) ∪ (C' ∖ {¬l})
```

Repeat until K reaches a "final" form suitable for backjumping.

---

### 5. Learn
```
M, F, D, K  ⊢  M, F ∪ {K}, D, K
```
**When:** K ≠ ∅, K ∉ F.
**Effect:** Add K to F as a **learned clause**. This is what makes CDCL powerful — the learned clause prevents revisiting the same conflict.

> K remains active for Backjump after Learn.

---

### 6. Backjump
```
M·l₀·M', F, D·l₀, K  ⊢  M·l, F, D, ∅
```
**When:** K ≠ ∅, ∃ literal `l ∈ K` and decision `l₀ ∈ D` such that:
- All literals in `K ∖ {l}` have their negations in M **before** l₀
- `¬l` appears in M at or after l₀

**Effect:**
1. Remove l₀ and everything after it from M
2. Remove l₀ from D (and everything after)
3. Add `l` to M as a **forced** (non-decision) literal
4. Clear K to ∅

The literal `l` is the **assertion literal** (the UIP in many implementations).
After backjump, K becomes a unit clause at the new level, immediately forcing `l`.

---

### 7. Fail (UNSAT)
```
M, F, ∅, K  ⊢  UNSAT
```
**When:** K ≠ ∅, D = ∅ (no decisions left to backjump to).
**Effect:** The formula is **UNSATISFIABLE**.

---

## Typical CDCL Flow

```
Initial state: M=∅, F, D=∅, K=∅

loop:
  1. Unit Propagate  (while unit clauses exist)
  2. If all clauses satisfied → SAT ✓
  3. Conflict         (set K when a clause is fully false)
  4. Explain          (resolve K with reason clauses, repeatedly)
  5. Learn            (add K to F)
  6. Backjump         (assert UIP literal, jump back)
     -- OR --
     Fail             (if D=∅ → UNSAT ✗)
  7. Goto 1
```

---

## Formula Input Syntax

Same as DPLL tutorial:
```
p | q, -p | r, p | -q     ← comma-separated clauses, | for OR, - for NOT
x1 & x2 | x3 & -x2 | x1  ← & also works as clause separator
```

---

## Example Walkthrough: `p|q, p|-q, -p|q, -p|-q` (UNSAT)

| Step | Action | M | D | K | Notes |
|------|--------|---|---|---|-------|
| 0 | — | ∅ | ∅ | ∅ | Initial |
| 1 | Decide p=T | {p} | {p} | ∅ | Free choice |
| 2 | Unit Prop → q | {p,q} | {p} | ∅ | `-p|q` unit since p=T |
| 3 | Conflict | {p,q} | {p} | {¬p,¬q} | `-p|-q` fully false |
| 4 | Explain | {p,q} | {p} | {¬p} | Resolve {¬p,¬q} with `-p|q` on q |
| 5 | Learn | {p,q} | {p} | {¬p} | Add `{¬p}` to F |
| 6 | Backjump | {¬p} | ∅ | ∅ | Assert ¬p, jump to before p |
| 7 | Unit Prop → q | {¬p,q} | ∅ | ∅ | `p|q` unit since p=F |
| 8 | Conflict | {¬p,q} | ∅ | {p,¬q} | `p|-q` fully false |
| 9 | Explain | {¬p,q} | ∅ | {¬q} | Resolve with learned `{¬p}` on p |
| 10 | Explain | {¬p,q} | ∅ | {p} | Resolve with `p|q` on q |
| 11 | Fail | — | ∅ | {p} | D=∅, UNSAT |

---

## Connection to Class 4 Code

The tutorial implements the inference rules from `class-4/cdcl-solver.py`:

```python
conflict(m, f, d, k)       →  Conflict button
explain(m, f, d, k)        →  Explain button   (one resolution step)
learn(m, f, d, k)          →  Learn button
backjump(m, f, d, k)       →  Backjump button
unit_propagate(m, f, d, k) →  Unit Propagate button
decide(m, f, d, k)         →  Decide button
fail(m, f, d, k)           →  Fail button
```

The state `(m, f, d, k)` in Python maps to `(M, F, D, K)` in the tutorial.
Learned clauses from `learn()` are displayed with a teal left border in F.
