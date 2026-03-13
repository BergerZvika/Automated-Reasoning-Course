(set-logic QF_UF)
(declare-sort S 0)
(declare-fun f (S) S)
(declare-fun g (S) S)
(declare-fun x1 () S)
(declare-fun x2 () S)

(assert (= x1 (g x1)))
(assert (= x2 (f x1)))

(check-sat)
