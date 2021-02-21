# -*- coding: utf-8 -*-
"""Reverse Bits

Reverse bits of a given 32 bits unsigned integer.

Example 1:

Input: 00000010100101000001111010011100
Output: 00111001011110000010100101000000
Explanation: The input binary string 00000010100101000001111010011100
represents the unsigned integer 43261596, so return 964176192 which its binary
representation is 00111001011110000010100101000000.
Example 2:

Input: 11111111111111111111111111111101
Output: 10111111111111111111111111111111
Explanation: The input binary string 11111111111111111111111111111101
represents the unsigned integer 4294967293, so return 3221225471 which its
binary representation is 10101111110010110010011101101001.

Note:

Note that in some languages such as Java, there is no unsigned integer type.
In this case, both input and output will be given as signed integer type and
should not affect your implementation, as the internal binary representation
of the integer is the same whether it is signed or unsigned.

In Java, the compiler represents the signed integers using 2's complement
notation. Therefore, in Example 2 above the input represents the signed integer
-3 and the output represents the signed integer -1073741825.

"""

from functools import reduce
import math
from collections import namedtuple


class Bits(object):
    __slots__ = ['__bin']

    @staticmethod
    def __to_bin32(n: int):
        b = bin(n)
        b32 = b[2 + b.find('0b'):]
        length = len(b32)
        return '0' * (32 - length) + b32

    @staticmethod
    def __reverse_str(s: str):
        def helper(s_: str, rec: str):
            if not s_:
                return rec
            else:
                return helper(s_[1:], s_[0] + rec)

        return helper(s, '')

    def __init__(self, n: int):
        self.__bin: str = Bits.__to_bin32(n)

    def reverse(self):
        return int(Bits.__reverse_str(self.__bin), 2)


if __name__ == '__main__':
    in1 = 43261596
    in2 = 4294967293
    exp1 = 964176192
    exp2 = 3221225471

    assert exp1 == Bits(in1).reverse()
    assert exp2 == Bits(in2).reverse()
