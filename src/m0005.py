"""Longest Palindromic Substring
TAG: untagged

Given a string s, find the longest palindromic substring in s. You may assume
that the maximum length of s is 1000.

Example 1:
Input: "babad"
Output: "bab"
Note: "aba" is also a valid answer.

Example 2:
Input: "cbbd"
Output: "bb"

"""

from functools import reduce


def solution(s: str) -> str:
    return reduce(lambda x, y: x + y,
                  (x1 for x1, x2 in zip(iter(s), reversed(s)) if x1 == x2), '')


if __name__ == '__main__':
    in1 = 'abcabcabaca'
    in2 = 'babad'
    in3 = 'cbbd'

    exp1 = 'aca'
    exp2 = 'aba'
    exp3 = 'bb'

    assert solution(in1) == exp1
    assert solution(in2) == exp2
    assert solution(in3) == exp3
