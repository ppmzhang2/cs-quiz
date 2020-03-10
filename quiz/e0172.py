# -*- coding: utf-8 -*-
"""Factorial Trailing Zeroes

Given an integer n, return the number of trailing zeroes in n!.

Example 1:

Input: 3
Output: 0
Explanation: 3! = 6, no trailing zero.
Example 2:

Input: 5
Output: 1
Explanation: 5! = 120, one trailing zero.
Note: Your solution should be in logarithmic time complexity.

"""

from functools import reduce
import math


def solution(n: int) -> int:
    if n <= 4:
        return 0
    else:
        order: int = math.floor(math.log(n, 5))
        return reduce(lambda x1, x2: x1 + x2,
                      map(lambda x: n // 5**x, range(1, order + 1)))


if __name__ == '__main__':
    in1 = 2
    exp1 = 0
    in2 = 5
    exp2 = 1
    in3 = 10
    exp3 = 2
    in4 = 24
    exp4 = 4
    in5 = 25
    exp5 = 6
    in6 = 69
    exp6 = 15
    in7 = 120
    exp7 = 28

    assert solution(in1) == exp1
    assert solution(in2) == exp2
    assert solution(in3) == exp3
    assert solution(in4) == exp4
    assert solution(in5) == exp5
    assert solution(in6) == exp6
    assert solution(in7) == exp7
