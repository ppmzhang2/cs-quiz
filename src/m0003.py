# -*- coding: utf-8 -*-
"""Longest Substring Without Repeating Characters

Given a string, find the length of the longest substring without repeating
characters.

Examples:

Given "abcabcbb", the answer is "abc", which the length is 3.

Given "bbbbb", the answer is "b", with the length of 1.

Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer
must be a substring, "pwke" is a subsequence and not a substring.

"""


class DP(object):
    """
    Dynamic Programming
    """
    @staticmethod
    def longest_substr_ending(s: str):
        if len(s) == 1:
            return s
        else:
            last = DP.longest_substr_ending(s[:-1])
            c = s[-1]
            if c in last:
                return c
            else:
                return last + c

    @staticmethod
    def longest_substr_gen(s: str):
        res = s[0]
        rem = s[1:]
        while True:
            yield res
            if not rem:
                break
            c = rem[0]
            if c in res:
                res = c
            else:
                res = res + c
            rem = rem[1:]

    @staticmethod
    def longest_substr(s: str):
        return max(DP.longest_substr_gen(s), key=lambda x: len(x))


if __name__ == '__main__':
    in1 = 'abcabcbb'
    in2 = 'bbbbb'
    in3 = 'pwwkew'
    exp1 = 'abc'
    exp2 = 'b'
    exp3 = 'wke'

    assert DP.longest_substr(in1) == exp1
    assert DP.longest_substr(in2) == exp2
    assert DP.longest_substr(in3) == exp3
