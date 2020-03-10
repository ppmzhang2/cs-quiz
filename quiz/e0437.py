# -*- coding: utf-8 -*-
"""Path Sum iii
You are given a binary tree in which each node contains an integer value.

Find the number of paths that sum to a given value.

The path does not need to start or end at the root or a leaf, but it must go
downwards (traveling only from parent nodes to child nodes).

The tree has no more than 1,000 nodes and the values are in the range
-1,000,000 to 1,000,000.

Example:

root = [10,5,-3,3,2,null,11,3,-2,null,1], sum = 8

      10
     /  \
    5   -3
   / |    \
  3   2   11
 / |   \
3  -2   1

Return 3. The paths that sum to 8 are:

1.  5 -> 3
2.  5 -> 2 -> 1
3. -3 -> 11

"""
from __future__ import annotations

from functools import reduce
from typing import Generator, Optional, Tuple
from adt.tree import Tree
from adt.zipper import ZipperTree


class PS(object):
    """
    prefix sum
    """
    @staticmethod
    def prefix_sum(arr: Tuple[int]) -> Tuple[int, ...]:
        def helper(arr_: Tuple[int], rec: Tuple[int, ...]):
            if not arr_:
                return rec
            else:
                return helper(arr_[1:], rec + (rec[-1] + arr_[0], ))

        return helper(arr, (0, ))

    @staticmethod
    def path_sum(arr: Tuple, target: int):
        def prefix_sums(arr_pre: Tuple, target: int):
            def helper(arr_pre_: Tuple, idx: int, target_: int):
                return tuple(
                    filter(lambda x: arr_pre_[idx] - arr_pre_[x] == target_,
                           range(idx - 1)))

            return reduce(
                lambda x, y: x + y,
                map(
                    lambda idx: [(i, idx)
                                 for i in helper(arr_pre, idx, target)],
                    range(len(arr_pre))))

        return prefix_sums(PS.prefix_sum(arr), target)


class NewZipperTree(ZipperTree):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def bottom_iter(self) -> Generator[Optional[NewZipperTree]]:
        return filter(lambda t: t.bottom_most,
                      super(NewZipperTree, self).bfs())

    def path_iter(self) -> Generator[Optional[NewZipperTree]]:
        t = self
        while True:
            yield t
            if t.top_most:
                break
            else:
                t = t.go_up()

    def paths_iter(
            self) -> Generator[Optional[Generator[Optional[NewZipperTree]]]]:
        bottoms = self.bottom_iter()
        return (tr.path_iter() for tr in bottoms)


if __name__ == '__main__':
    tr1 = Tree(node=1,
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
    zt1 = NewZipperTree(tree=tr1)

    # for i in zt1.bottom_iter():
    #     print(type(i))
    #     print(i.tree.node)

    # for i in zt1.go_bottomleft().path_iter():
    #     print(type(i))
    #     print(i.tree.node)

    # for path in zt1.paths_iter():
    #     print('new path:')
    #     for zt in path:
    #         print(zt.tree.node)

    # print(PS.path_sum([1, 2, 3, 4, 5], 6))

    for path in zt1.paths_iter():
        tp = tuple(i.tree.node for i in path)
        print('new path:')
        print(tp)
        print(PS.path_sum(tp, 8))
        print([tp[i[0]:i[1]] for i in PS.path_sum(tp, 8)])
