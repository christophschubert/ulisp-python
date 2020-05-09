(def add-two (a) (+ a 2))
(def hurz (a b c) (+ c (+ a (add-two b))))
(def main () (hurz 3000 200 10))
