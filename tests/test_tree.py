import unittest
from adt.tree import BTree


class TestBTree(unittest.TestCase):
    ibt1 = BTree(node=3,
                 left=BTree(node=9),
                 right=BTree(node=20, left=BTree(node=15),
                             right=BTree(node=7)))
    ibt2 = BTree(node=1,
                 left=BTree(node=2, left=BTree(node=3, left=BTree(node=4))),
                 right=BTree(node=5,
                             left=BTree(node=6),
                             right=BTree(node=7,
                                         left=BTree(node=8),
                                         right=BTree(9))))

    def test_depth(self):
        ibt1_depth = 3
        ibt2_depth = 4
        self.assertEqual(ibt1_depth, self.ibt1.depth())
        self.assertEqual(ibt2_depth, self.ibt2.depth())

    def test_traverse(self):
        ibt2_bfs = (1, 2, 5, 3, 6, 7, 4, 8, 9)
        ibt2_dfs_pre = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        ibt2_dfs_in = (4, 3, 2, 1, 6, 5, 8, 7, 9)
        ibt2_dfs_post = (4, 3, 2, 6, 8, 9, 7, 5, 1)
        self.assertEqual(ibt2_bfs, self.ibt2.bfs())
        self.assertEqual(ibt2_dfs_pre, self.ibt2.dfs_pre())
        self.assertEqual(ibt2_dfs_in, self.ibt2.dfs_in())
        self.assertEqual(ibt2_dfs_post, self.ibt2.dfs_post())


if __name__ == '__main__':
    unittest.main(verbosity=2)
