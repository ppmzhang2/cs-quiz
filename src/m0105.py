"""construct binary tree from pre-order and in-order traversal
Given pre-order and in-order traversal of a tree, construct the binary tree.

Note:

You may assume that duplicates do not exist in the tree

Example:

pre-order: [3, 9, 20, 15, 7]
in-order: [9, 3, 15, 20, 7]

output:

        3
       / \
      9  20
        /  \
       15   7
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class BTree:
    root: T
    left: Optional[T]
    right: Optional[T]


if __name__ == '__main__':
    ipt_1_1 = [3, 9, 20, 15, 7]
    ipt_1_2 = [9, 3, 15, 20, 7]
