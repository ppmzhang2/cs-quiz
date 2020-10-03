# -*- coding: utf-8 -*-
from __future__ import annotations

from functools import reduce
from itertools import chain
from typing import Any, Callable, Iterable, List, NamedTuple, Optional, Tuple

from adt.stack import Stack


class Tree(NamedTuple):
    """
    Immutable Tree
    """
    node: Any
    children: Tuple[Tree, ...] = ()

    @property
    def is_leaf(self):
        return self.children == ()

    @classmethod
    def _dfs_helper(cls, stack: Stack, acc: Tuple[Any, ...],
                    cb: Callable[[Tree], Iterable[Tree]]):
        """depth-first search helper
        depth-first search is like manipulating a stack: get a tree in a stack,
        then pop it out and push into the stack its node value and its children
        (the order is depending on whether this is a pre-order or post-order
        search). Repeat this step until the stack is empty

        :param stack: stack to keep the tree
        :param acc: sequence of the search result
        :param cb: callback function to arrange the node and the children of
          the tree popped out
        """
        while True:
            if stack.empty():
                break

            tree: Tree = stack.pop()
            if tree.is_leaf:
                acc = acc + (tree.node, )
            else:
                items = cb(tree)
                for child in items:
                    stack.push(child)

        return acc

    @staticmethod
    def __bfs(tp: Tuple[Tree, ...]) -> Tuple[Tree, ...]:
        return reduce(
            lambda x, y: x + tuple(
                filter(lambda tr: tr is not None, y.children)), tp, ())

    def bfs(self) -> Tuple[Any, ...]:
        """Breadth-first search

        :return:
        """
        def helper(tp: Tuple[Tree, ...],
                   rec: Tuple[Any, ...]) -> Tuple[Any, ...]:
            if not tp:
                return rec
            else:
                rec_ = rec + tuple(i.node for i in tp)
                return helper(Tree.__bfs(tp), rec_)

        return helper((self, ), ())

    def dfs_pre(self) -> Tuple[Any, ...]:
        def callback(tree: Tree):
            return chain(reversed(tree.children), (Tree(node=tree.node), ))

        return self._dfs_helper(Stack((self, )), (), callback)

    def dfs_post(self) -> Tuple[Any, ...]:
        def callback(tree: Tree):
            return chain((Tree(node=tree.node), ), reversed(tree.children))

        return self._dfs_helper(Stack((self, )), (), callback)

    def depth(self) -> int:
        """check binary tree depth with depth-first search

        :return: tree depth
        """
        def helper(tp: Tuple[Tree, ...], rec: int) -> int:
            if not tp:
                return rec
            else:
                return helper(Tree.__bfs(tp), rec + 1)

        return helper((self, ), 0)


class BTree(Tree):
    """
    Immutable Binary Tree
    """
    def __new__(cls, node: Any, left: BTree = None, right: BTree = None):
        children: Tuple[Optional[BTree], ...] = tuple(
            filter(lambda t: t is not None, (left, right)))
        self = super().__new__(cls, node, children)
        self.left = left
        self.right = right
        return self

    @staticmethod
    def __dfs_in(tp: Tuple[BTree, ...]) -> Tuple[BTree, ...]:
        bt = tp[0]
        return tuple(
            filter(lambda tr: tr is not None,
                   (bt.left, BTree(node=bt.node), bt.right))) + tp[1:]

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

    def dfs_in(self) -> Tuple[Any, ...]:
        return self.__dfs(BTree.__dfs_in)
