# -*- coding: utf-8 -*-
"""Maximum Depth of Binary Tree
TAG: binary-tree

Given a binary tree, find its maximum depth.

The maximum depth is the number of nodes along the longest path from the root
node down to the farthest leaf node.

Note: A leaf is a node with no children.

Example:

Given binary tree [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
return its depth = 3.

        1
       / \
      2  5
     /  / \
    3  6   7
   /      / \
  4      8   9

"""

from __future__ import annotations
from typing import NamedTuple, Tuple
from functools import reduce


class BTree(NamedTuple):
    node: int
    left: BTree = None
    right: BTree = None


class Rec(object):
    """
    Recursive
    """
    @staticmethod
    def depth(bt: BTree) -> int:
        if bt is None:
            return 0
        else:
            return max(Rec.depth(bt.left), Rec.depth(bt.right)) + 1


class Tt(object):
    """
    tree traversal based methods
    """
    @staticmethod
    def __bfs(tp: Tuple[BTree, ...]) -> Tuple[BTree, ...]:
        return reduce(
            lambda x, y: x + tuple(
                filter(lambda tr: tr is not None, (y.left, y.right))), tp, ())

    @staticmethod
    def __dfs_pre(tp: Tuple[BTree, ...]) -> Tuple[BTree, ...]:
        bt = tp[0]
        return tuple(
            filter(lambda tr: tr is not None,
                   (BTree(node=bt.node), bt.left, bt.right))) + tp[1:]

    @staticmethod
    def __dfs_in(tp: Tuple[BTree, ...]) -> Tuple[BTree, ...]:
        bt = tp[0]
        return tuple(
            filter(lambda tr: tr is not None,
                   (bt.left, BTree(node=bt.node), bt.right))) + tp[1:]

    @staticmethod
    def __dfs_post(tp: Tuple[BTree, ...]) -> Tuple[BTree, ...]:
        bt = tp[0]
        return tuple(
            filter(lambda tr: tr is not None,
                   (bt.left, bt.right, BTree(node=bt.node)))) + tp[1:]

    @staticmethod
    def bfs(bt: BTree) -> Tuple[int]:
        """Breadth-first search

        :param bt:
        :return:
        """
        def helper(tp: Tuple[BTree, ...],
                   rec: Tuple[int, ...]) -> Tuple[int, ...]:
            if not tp:
                return rec
            else:
                rec_ = rec + tuple(i.node for i in tp)
                return helper(Tt.__bfs(tp), rec_)

        return helper((bt, ), ())

    @staticmethod
    def __dfs(bt: BTree, cb):
        def helper(tp: Tuple[BTree, ...],
                   rec: Tuple[int, ...]) -> Tuple[int, ...]:
            if not tp:
                return rec
            elif tp[0].left is None and tp[0].right is None:
                return helper(tp[1:], rec + (tp[0].node, ))
            else:
                return helper(cb(tp), rec)

        return helper((bt, ), ())

    @staticmethod
    def dfs_pre(bt: BTree) -> Tuple[int, ...]:
        return Tt.__dfs(bt, Tt.__dfs_pre)

    @staticmethod
    def dfs_in(bt: BTree) -> Tuple[int, ...]:
        return Tt.__dfs(bt, Tt.__dfs_in)

    @staticmethod
    def dfs_post(bt: BTree) -> Tuple[int, ...]:
        return Tt.__dfs(bt, Tt.__dfs_post)

    @staticmethod
    def depth(bt: BTree) -> int:
        """check binary tree depth with depth-first search

        :param bt: binary tree
        :return: tree depth
        """
        def helper(tp: Tuple[BTree, ...], rec: int) -> int:
            if not tp:
                return rec
            else:
                return helper(Tt.__bfs(tp), rec + 1)

        return helper((bt, ), 0)


if __name__ == '__main__':
    bt1 = BTree(node=3,
                left=BTree(node=9),
                right=BTree(node=20, left=BTree(node=15), right=BTree(node=7)))
    exp_depth1 = 3
    exp_bfs1 = (3, 9, 20, 15, 7)

    bt2 = BTree(node=1,
                left=BTree(node=2, left=BTree(node=3, left=BTree(node=4))),
                right=BTree(node=5,
                            left=BTree(node=6),
                            right=BTree(node=7,
                                        left=BTree(node=8),
                                        right=BTree(9))))
    exp_depth2 = 4
    exp_bfs2 = (1, 2, 5, 3, 6, 7, 4, 8, 9)
    exp_dfs_pre2 = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    exp_dfs_in2 = (4, 3, 2, 1, 6, 5, 8, 7, 9)
    exp_dfs_post2 = (4, 3, 2, 6, 8, 9, 7, 5, 1)

    assert exp_bfs1 == Tt.bfs(bt1)
    assert exp_depth1 == Tt.depth(bt1)
    assert exp_depth2 == Tt.depth(bt2)
    assert exp_bfs2 == Tt.bfs(bt2)
    assert exp_dfs_pre2 == Tt.dfs_pre(bt2)
    assert exp_dfs_in2 == Tt.dfs_in(bt2)
    assert exp_dfs_post2 == Tt.dfs_post(bt2)
