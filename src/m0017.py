"""Letter Combinations of a Phone Number
TAG: back-tracking

Given a string containing only numbers from 2 to 9, return all the alphabetic
combinations. The mapping from letters to numbers is the same with phone keys.

Examples:

* input："23"
* output：["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
"""

from itertools import product
from typing import Tuple


class PhoneLetters(object):
    DC = {
        '2': ('a', 'b', 'c'),
        '3': ('d', 'e', 'f'),
        '4': ('g', 'h', 'i'),
        '5': ('j', 'k', 'l'),
        '6': ('m', 'n', 'o'),
        '7': ('p', 'q', 'r', 's'),
        '8': ('t', 'u', 'v'),
        '9': ('w', 'x', 'y', 'z')
    }

    @staticmethod
    def _cartesian_product(seq1: Tuple[str, ...],
                           seq2: Tuple[str, ...]) -> Tuple[str, ...]:
        return tuple(i + j for i, j in product(seq1, seq2))

    @classmethod
    def solution(cls, s: str):
        def helper(seq: Tuple[str, ...], acc: Tuple[str, ...]):
            if not seq:
                return acc
            else:
                return helper(seq[1:],
                              cls._cartesian_product(acc, cls.DC[seq[0]]))

        return set(helper(tuple(c for c in s), ('', )))


if __name__ == '__main__':
    input_1 = '23'
    exp_1 = {'ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf'}

    pl = PhoneLetters()

    assert pl.solution(input_1) == exp_1
