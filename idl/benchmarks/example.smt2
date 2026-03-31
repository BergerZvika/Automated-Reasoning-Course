; IDL example from lecture slides — UNSAT (negative cycle x→z→w→x, weight -2)
(set-logic QF_IDL)
(declare-const x Int)
(declare-const y Int)
(declare-const z Int)
(declare-const w Int)
(assert (<= (- x y)    5))   ; x - y <= 5
(assert (<= (- y x)   -5))   ; y - x <= -5
(assert (<= (- y z)   -2))   ; y - z <= -2
(assert (<= (- x z)   -3))   ; x - z <= -3
(assert (<= (- w x)    2))   ; w - x <= 2
(assert (<= (- x w)   -2))   ; x - w <= -2
(assert (<= (- z w)   -1))   ; z - w <= -1
(check-sat)
; Expected: unsat
; Negative cycle: x -> z (-3) -> w (-1) -> x (2), total = -2
