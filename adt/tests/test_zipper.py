# -*- coding: utf-8 -*-
"""test for ADT.zipper
Test Cases:

ZipperCons:

1 -> 2 -> 3 -> 4
"""

import unittest

from adt.cons import Cons
from adt.zipper import ZipperCons


class ZipperConsTest(unittest.TestCase):
    cons = Cons(car=1,
                cdr=Cons(car=2, cdr=Cons(car=3, cdr=Cons(car=4, cdr=None))))
    len_cons = 4

    def test_zipper_cons(self):
        zc1 = ZipperCons.from_cons(cons=ZipperConsTest.cons)
        zc2 = zc1.go_right().go_left()
        zc3 = zc1.go_right().go_right().go_left().go_left()
        zc4 = zc1.go_right_most().go_left_most()
        self.assertEqual(zc1, zc2)
        self.assertEqual(zc1, zc3)
        self.assertEqual(zc1, zc4)
        self.assertEqual(ZipperConsTest.len_cons, len(zc1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
