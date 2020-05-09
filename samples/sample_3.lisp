(def add-two (a) (+ a 2))
(def hurz (a b) (+ a (add-two b)))
(def schnurz (a b c) (+ a (hurz a (hurz b c))))
(def main () (schnurz 40 20 30))
