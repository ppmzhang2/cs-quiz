# -*- coding: utf-8 -*-
"""Number of 1 Bits

Write a function that takes an unsigned integer and return the number of '1'
bits it has (also known as the Hamming weight).

Example 1:

Input: 00000000000000000000000000001011
Output: 3
Explanation: The input binary string 00000000000000000000000000001011 has a
total of three '1' bits.
Example 2:

Input: 00000000000000000000000010000000
Output: 1
Explanation: The input binary string 00000000000000000000000010000000 has a
total of one '1' bit.
Example 3:

Input: 11111111111111111111111111111101
Output: 31
Explanation: The input binary string 11111111111111111111111111111101 has a
total of thirty one '1' bits.

Note:

Note that in some languages such as Java, there is no unsigned integer type.
In this case, the input will be given as signed integer type and should not
affect your implementation, as the internal binary representation of the
integer is the same whether it is signed or unsigned.

In Java, the compiler represents the signed integers using 2's complement
notation. Therefore, in Example 3 above the input represents the signed
integer -3.

"""

from functools import reduce
import math
from collections import namedtuple


class CL(object):
    """
    Count from left
    """
    @staticmethod
    def ones(n: int):
        def helper(n_: int, rec: int):
            if not n_:
                return rec
            else:
                order = math.floor(math.log(n_, 2))
                return helper(n_ - 2**order, rec + 1)

        return helper(n, 0)


class CR(object):
    """
    Count from right
    """
    @staticmethod
    def ones(n: int):
        def helper(n_: int, rec: int):
            if not n_:
                return rec
            else:
                return helper(n_ & n_ - 1, rec + 1)

        return helper(n, 0)


if __name__ == '__main__':
    in1 = 43261596
    in2 = 4294967293
    exp1 = 12
    exp2 = 31

    assert CL.ones(in1) == exp1
    assert CL.ones(in2) == exp2
    assert CR.ones(in1) == exp1
    assert CR.ones(in2) == exp2
