;; test1_congruence.smt2
(set-logic QF_UF)
(declare-sort U 0)
(declare-fun f (U) U)
(declare-const x U)
(declare-const y U)

(assert (= x y))
(assert (not (= (f x) (f y))))

(check-sat)