# -*- coding: utf-8 -*-
"""Single Number

Given a non-empty array of integers, every element appears twice except for
one. Find that single one.

Note:

Your algorithm should have a linear runtime complexity. Could you implement
it without using extra memory?

"""

from functools import reduce
from typing import Tuple


def solution(arr: Tuple[int, ...]) -> int:
    return reduce(lambda x, y: x ^ y, arr)


if __name__ == '__main__':
    in1 = (1, 2, 3, 4, 5, 3, 2, 1, 4)
    exp1 = 5

    assert exp1 == solution(in1)
