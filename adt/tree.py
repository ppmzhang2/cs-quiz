# -*- coding: utf-8 -*-
from __future__ import annotations
from functools import reduce
from typing import Tuple, NamedTuple, Any


class BTree(NamedTuple):
    node: Any
    left: BTree = None
    right: BTree = None
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

    def bfs(self) -> Tuple[Any, ...]:
        """Breadth-first search

        :return:
        """
        def helper(tp: Tuple[BTree, ...],
                   rec: Tuple[Any, ...]) -> Tuple[Any, ...]:
            if not tp:
                return rec
            else:
                rec_ = rec + tuple(i.node for i in tp)
                return helper(BTree.__bfs(tp), rec_)

        return helper((self, ), ())

    def __dfs(self, cb):
        def helper(tp: Tuple[BTree, ...],
                   rec: Tuple[Any, ...]) -> Tuple[Any, ...]:
            if not tp:
                return rec
            elif tp[0].left is None and tp[0].right is None:
                return helper(tp[1:], rec + (tp[0].node, ))
            else:
                return helper(cb(tp), rec)

        return helper((self, ), ())

    def dfs_pre(self) -> Tuple[Any, ...]:
        return self.__dfs(BTree.__dfs_pre)

    def dfs_in(self) -> Tuple[Any, ...]:
        return self.__dfs(BTree.__dfs_in)

    def dfs_post(self) -> Tuple[Any, ...]:
        return self.__dfs(BTree.__dfs_post)

    def depth(self) -> int:
        """check binary tree depth with depth-first search

        :return: tree depth
        """
        def helper(tp: Tuple[BTree, ...], rec: int) -> int:
            if not tp:
                return rec
            else:
                return helper(BTree.__bfs(tp), rec + 1)

        return helper((self, ), 0)
