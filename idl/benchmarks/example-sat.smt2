; IDL example — SAT (same as slide but without x - w <= -2, breaking the negative cycle)
(set-option :produce-models true)
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
(assert (<= (- z w)   -1))   ; z - w <= -1
(check-sat)
(get-model)
; Expected: sat
