# -*- coding: utf-8 -*-
"""Generate Parentheses
n represents number of parentheses, design a function to generate all VALID
parentheses combination

demo:

input: n = 3
output: [
       "((()))",
       "(()())",
       "(())()",
       "()(())",
       "()()()"
     ]
"""
from __future__ import annotations

from typing import Tuple

from itertools import permutations


class Filter(object):
    DC = {
        1: '(',
        -1: ')',
    }

    @staticmethod
    def valid(seq: Tuple[int, ...]):
        def helper(seq_: Tuple[int, ...], acc: int = 0):
            while acc >= 0 and len(seq_) > 0:
                seq_, acc = seq_[1:], acc + seq_[0]

            if acc < 0:
                return False
            else:
                return True

        return helper(seq, 0)


class Recursion(object):
    @staticmethod
    def solution(n: int):
        ls = set()

        def helper(output, first, last, input):
            if first == input and last == input:
                ls.add(output)
            else:
                if first < input:
                    helper(output + "(", first + 1, last, input)
                if last < first:
                    helper(output + ")", first, last + 1, input)

        helper("", 0, 0, n)
        return ls


if __name__ == '__main__':
    input_1 = 3
    exp_1 = {"((()))", "(()())", "(())()", "()(())", "()()()"}
    assert Recursion.solution(input_1) == exp_1
