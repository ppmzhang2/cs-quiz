# -*- coding: utf-8 -*-
"""Valid Palindrome

Given a string, determine if it is a palindrome, considering only alphanumeric
characters and ignoring cases.

Note: For the purpose of this problem, we define empty string as valid
palindrome.

Example 1:

Input: "A man, a plan, a canal: Panama"
Output: true
Example 2:

Input: "race a car"
Output: false

"""


def solution(pattern: str) -> bool:
    if len(pattern) <= 1:
        return True
    elif not pattern[0].isalpha():
        return solution(pattern[1:])
    elif not pattern[-1].isalpha():
        return solution(pattern[:-1])
    elif pattern[0].lower() != pattern[-1].lower():
        return False
    else:
        return solution(pattern[1:-1])


if __name__ == '__main__':
    in1 = "A man, a plan, a canal: Panama"
    exp1 = True
    in2 = "race a car"
    exp2 = False

    assert exp1 == solution(in1)
    assert exp2 == solution(in2)
