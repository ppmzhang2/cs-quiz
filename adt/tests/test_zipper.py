# -*- coding: utf-8 -*-
"""test for ADT.zipper
Test Cases:

Tree:

        1
       /|\
      2 3 4
     /  |  \
    5   6   7
   /      / | \
  8      9 10  11

ZipperCons:

1 -> 2 -> 3 -> 4
"""

import unittest

from adt.cons import Cons
from adt.tree import Tree
from adt.zipper import ZipperCons, ZipperTree


class ZipperConsTest(unittest.TestCase):
    tr = Tree(node=1,
              children=(
                  Tree(
                      node=2,
                      children=(Tree(node=5, children=(Tree(node=8), )), ),
                  ),
                  Tree(node=3, children=(Tree(node=6), )),
                  Tree(node=4,
                       children=(Tree(node=7,
                                      children=(Tree(node=9), Tree(node=10),
                                                Tree(node=11))), )),
              ))
    tr_bfs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    tr_dfs_pre = (1, 2, 5, 8, 3, 6, 4, 7, 9, 10, 11)
    tr_dfs_post = (8, 5, 2, 6, 3, 9, 10, 11, 7, 4, 1)
    cons = Cons(car=1,
                cdr=Cons(car=2, cdr=Cons(car=3, cdr=Cons(car=4, cdr=None))))
    len_cons = 4
    cons_slice = Cons(car=4, cdr=Cons(car=2, cdr=None))

    def test_zipper_tree(self):
        zt = ZipperTree(tree=self.tr)
        zt_bfs = tuple(t.tree.node for t in zt.bfs())
        zt_dfs_pre = tuple(t.tree.node for t in zt.dfs_pre())
        zt_dfs_post = tuple(t.tree.node for t in zt.dfs_post())
        self.assertEqual(self.tr_bfs, zt_bfs)
        self.assertEqual(self.tr_dfs_pre, zt_dfs_pre)
        self.assertEqual(self.tr_dfs_post, zt_dfs_post)

    def test_zipper_cons(self):
        zc1 = ZipperCons.from_cons(cons=self.cons)
        zc2 = zc1.go_right().go_left()
        zc3 = zc1.go_right().go_right().go_left().go_left()
        zc4 = zc1.go_right_most().go_left_most()
        self.assertEqual(zc1, zc2)
        self.assertEqual(zc1, zc3)
        self.assertEqual(zc1, zc4)
        self.assertEqual(self.len_cons, len(zc1))
        self.assertEqual(self.cons_slice, zc1[3:0:-2])
        with self.assertRaises(IndexError):
            zc1[4]
        with self.assertRaises(IndexError):
            zc1[-5]


if __name__ == '__main__':
    unittest.main(verbosity=2)
