# -*- coding: utf-8 -*-
"""Ugly Number
Write a program to check whether a given number is an ugly number.

Ugly numbers are positive numbers whose prime factors only include 2, 3, 5.

Example 1:

Input: 6
Output: true
Explanation: 6 = 2 × 3
Example 2:

Input: 8
Output: true
Explanation: 8 = 2 × 2 × 2
Example 3:

Input: 14
Output: false
Explanation: 14 is not ugly since it includes another prime factor 7.
Note:

1 is typically treated as an ugly number.
Input is within the 32-bit signed integer range: [−231,  231 − 1].

"""


class Rc(object):
    """
    recursive solution
    """
    @staticmethod
    def solution(n: int):
        if n == 1:
            return True
        elif n % 5 == 0:
            return Rc.solution(n // 5)
        elif n % 3 == 0:
            return Rc.solution(n // 3)
        elif n % 2 == 0:
            return Rc.solution(n // 2)
        else:
            return False


if __name__ == '__main__':
    in1 = 8
    in2 = 6
    in3 = 14
    in4 = 29
    exp1 = True
    exp2 = True
    exp3 = False
    exp4 = False

    assert Rc.solution(in1) is exp1
    assert Rc.solution(in2) is exp2
    assert Rc.solution(in3) is exp3
    assert Rc.solution(in4) is exp4
