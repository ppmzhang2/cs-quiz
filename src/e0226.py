# -*- coding: utf-8 -*-
"""Invert Binary Tree
TAG: binary-tree

Invert a binary tree.

Example:

Input:

     4
   /   \
  2     7
 / \   / \
1   3 6   9
Output:

     4
   /   \
  7     2
 / \   / \
9   6 3   1
Trivia:
This problem was inspired by this original tweet by Max Howell:

Google: 90% of our engineers use the software you wrote (Homebrew), but
you can’t invert a binary tree on a whiteboard so f*** off.

"""

from __future__ import annotations
from typing import NamedTuple, Tuple, Union
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
    def solution(bt: BTree) -> Union[BTree, None]:
        if bt is None:
            return bt
        else:
            return BTree(node=bt.node,
                         left=Rec.solution(bt.right),
                         right=Rec.solution(bt.left))


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

    bt2 = BTree(node=1,
                left=BTree(node=2, left=BTree(node=3, left=BTree(node=4))),
                right=BTree(node=5,
                            left=BTree(node=6),
                            right=BTree(node=7,
                                        left=BTree(node=8),
                                        right=BTree(9))))

    print(Rec.solution(bt1))
