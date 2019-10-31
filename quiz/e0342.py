# -*- coding: utf-8 -*-
"""Power of Four
Given an integer (signed 32 bits), write a function to check whether it is a
power of 4.

Example 1:
Input: 16
Output: true

Example 2:
Input: 5
Output: false

Follow up: Could you solve it without loops/recursion?

"""
import math


class Log(object):
    """
    with logarithm
    """
    @staticmethod
    def solution(n: int):
        power = math.floor(math.log(n, 4))
        if n > 4**power:
            return False
        else:
            return True


class Dec(object):
    """
    solve with decimal system
    """
    @staticmethod
    def __2power(n: int):
        if n & (n - 1) == 0:
            return True
        else:
            return False

    @staticmethod
    def solution(n: int):
        m = int(
            '1010101010101010101010101010101010101010101101010101010101010101',
            2)
        res = m & n
        if Dec.__2power(n) and res == n:
            return True
        else:
            return False


if __name__ == '__main__':
    in1 = 16
    in2 = 5
    exp1 = True
    exp2 = False

    assert Log.solution(in1) is exp1
    assert Log.solution(in2) is exp2
    assert Dec.solution(in1) is exp1
    assert Dec.solution(in2) is exp2
