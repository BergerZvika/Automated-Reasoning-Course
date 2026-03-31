; IDL example — SAT
; Same graph as the slide but z - w <= 2 (instead of -1), breaking the negative cycle.
; Cycle x→z→w→x now has weight -3 + 2 + 2 = 1 > 0  →  no negative cycle  →  SAT
(set-option :produce-models true)
(set-logic QF_IDL)
(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(declare-const w Int)
(assert (<= (- x y)    5))   ; x - y <= 5
(assert (<= (- y x) (- 5)))  ; y - x <= -5
(assert (<= (- y z) (- 2)))  ; y - z <= -2
(assert (<= (- x z) (- 3)))  ; x - z <= -3
(assert (<= (- w x)    2))   ; w - x <= 2
(assert (<= (- z w)    2))   ; z - w <= 2  (was -1 in the UNSAT example)
(check-sat)
(get-model)
; Expected: sat
