"""Divide Two Integers
TAG: binary-search, math

Given two integers dividend and divisor, divide two integers without using
multiplication, division and mod operator.

Return the quotient after dividing dividend by divisor.

The integer division should truncate toward zero.

Example 1:

Input: dividend = 10, divisor = 3
Output: 3

Example 2:

Input: dividend = 7, divisor = -3
Output: -2

Note:

Both dividend and divisor will be 32-bit signed integers.
The divisor will never be 0.
Assume we are dealing with an environment which could only store integers within
the 32-bit signed integer range: [−231,  231 − 1]. For the purpose of this
problem, assume that your function returns 231 − 1 when the division result
overflows.
"""
from __future__ import annotations

from typing import Any, Optional


class Bisection(object):
    @staticmethod
    def solution(dividend, divisor):
        def helper(dividend_, divisor_):
            res_ = 0
            i_ = 1
            _dividend_ = dividend_
            _divisor_ = divisor_
            while True:
                if _dividend_ < _divisor_:
                    break
                _dividend_ -= _divisor_
                _divisor_ += _divisor_
                res_ += i_
                i_ += i_
            return res_, _dividend_

        rec = 0
        dividend__ = dividend
        while True:
            res, dividend__ = helper(dividend__, divisor)
            if res == 0:
                break
            rec += res

        return rec


if __name__ == '__main__':
    input_1_1 = 113
    input_1_2 = 3
    exp_1 = 37
    assert Bisection.solution(input_1_1, input_1_2) == exp_1
