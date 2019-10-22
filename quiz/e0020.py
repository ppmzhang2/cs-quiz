# -*- coding: utf-8 -*-
"""Valid Parentheses

Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.

Example 1:

Input: "()"
Output: true
Example 2:

Input: "()[]{}"
Output: true
Example 3:

Input: "(]"
Output: false
Example 4:

Input: "([)]"
Output: false
Example 5:

Input: "{[]}"
Output: true

"""

from collections import namedtuple

DataColl = namedtuple('DataColl', ('cate', 'head'))

alphabet = {
    '(': DataColl(cate=1, head=True),
    ')': DataColl(cate=1, head=False),
    '[': DataColl(cate=2, head=True),
    ']': DataColl(cate=2, head=False),
    '{': DataColl(cate=3, head=True),
    '}': DataColl(cate=3, head=False),
}


def is_valid(pattern: str) -> bool:
    def match(ch: chr):
        return alphabet[ch]

    def helper(s: str, rec: str) -> bool:
        # valid if empty string
        if s == '' and rec == '':
            return True
        # invalid if open brackets not closed
        elif s == '' and rec != '':
            return False
        # push heads to recursion arg
        elif match(s[0]).head is True:
            return helper(s[1:], s[0] + rec)
        # decide if the bracket closing is valid
        else:
            if match(s[0]).cate != match(rec[0]).cate:
                return False
            else:
                return helper(s[1:], rec[1:])

    return helper(pattern, '')


if __name__ == '__main__':
    in1 = '()'
    in2 = '()[]{}'
    in3 = '(]'
    in4 = '([)]'
    in5 = '{[]}'
    in6 = ''
    in7 = '(['
    exp1 = True
    exp2 = True
    exp3 = False
    exp4 = False
    exp5 = True
    exp6 = True
    exp7 = False

    assert is_valid(in1) == exp1
    assert is_valid(in2) == exp2
    assert is_valid(in3) == exp3
    assert is_valid(in4) == exp4
    assert is_valid(in5) == exp5
    assert is_valid(in6) == exp6
    assert is_valid(in7) == exp7
