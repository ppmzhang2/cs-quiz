"""test for ADT.cons

"""

import unittest

from adt.cons import Cons


class ConsTest(unittest.TestCase):
    def test_traversal(self):
        c1 = Cons(1, Cons(2, Cons(3, Cons(4))))
        c1_traversal = (1, 2, 3, 4)
        self.assertEqual(tuple(c1.traversal()), c1_traversal)

    def test_constr(self):
        c1_tuple = (2, 4, 6, 0, 1)
        c1 = Cons(2, Cons(4, Cons(6, Cons(0, Cons(1)))))
        self.assertEqual(Cons.constr(c1_tuple), c1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
