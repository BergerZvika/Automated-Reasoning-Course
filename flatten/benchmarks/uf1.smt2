(set-logic QF_UF)
(declare-sort S 0)
(declare-fun f (S) S)
(declare-fun g (S) S)
(declare-fun h (S) S)
(declare-fun x1 () S)
(declare-fun x2 () S)

(assert (= (g (f x1)) (g x1)))
(assert (distinct (f x1) x2))

(check-sat)
