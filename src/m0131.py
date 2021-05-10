"""Palindrome Partitioning
Given a string s, partition s such that every substring of the partition is a
palindrome. Return all possible palindrome partitioning of s.

A palindrome string is a string that reads the same backward as forward.

Example 1:
Input: s = "aab"
Output: [["a","a","b"],["aa","b"]]

Example 2:
Input: s = "a"
Output: [["a"]]

Constraints:
* 1 <= s.length <= 16
* s contains only lowercase English letters.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Tuple


@unique
class State(IntEnum):
    DONE = 0
    MERGE_AND_MOVE = 1
    CANNOT_MERGE = 2
    CANNOT_MOVE = 3
    INVALID = 4


@dataclass(frozen=True)
class FSM:
    pattern: str
    remains: str
    acc: Tuple[str, ...]

    @property
    def pattern_length(self) -> int:
        return len(self.pattern)

    @property
    def remaining_length(self) -> int:
        return len(self.remains)

    @property
    def palindrome(self) -> bool:
        idx_left = 0
        idx_right = self.pattern_length - 1
        while True:
            if idx_right - idx_left <= 0:
                return True
            if self.pattern[idx_left] != self.pattern[idx_right]:
                return False
            idx_left, idx_right = idx_left + 1, idx_right - 1

    @property
    def state(self) -> State:
        if self.remaining_length == 0 and not self.palindrome:
            return State.INVALID
        if (self.remaining_length == 0 and self.palindrome
                and self.pattern_length == 0):
            return State.DONE
        if (self.remaining_length == 0 and self.palindrome
                and self.pattern_length > 0):
            return State.CANNOT_MOVE
        if self.pattern_length == 0:
            return State.CANNOT_MERGE
        if not self.palindrome:
            return State.CANNOT_MERGE
        return State.MERGE_AND_MOVE

    def merge(self) -> FSM:
        return (type(self))('', self.remains, (*self.acc, self.pattern))

    def move(self) -> FSM:
        char, remains = self.remains[0], self.remains[1:]
        return (type(self))(self.pattern + char, remains, self.acc)


class PalindromePartitioning:
    @staticmethod
    def looper(
        inputs: Tuple[FSM, ...],
        outputs: Tuple[Tuple[str, ...], ...],
    ) -> Tuple[Tuple[str, ...], ...]:
        while True:
            if not inputs:
                return outputs
            fsm = inputs[0]
            if fsm.state == State.DONE:
                inputs, outputs = inputs[1:], (*outputs, fsm.acc)
            elif fsm.state == State.INVALID:
                inputs = inputs[1:]
            elif fsm.state == State.CANNOT_MERGE:
                inputs = (fsm.move(), *inputs[1:])
            elif fsm.state == State.CANNOT_MOVE:
                inputs = (fsm.merge(), *inputs[1:])
            else:
                inputs = (fsm.merge(), fsm.move(), *inputs[1:])

    def solution(self, chars: str):
        fsm = FSM('', chars, ())
        return tuple(sorted(self.looper((fsm, ), ())))


if __name__ == '__main__':
    ipt_1 = 'aab'
    exp_1 = (('a', 'a', 'b'), ('aa', 'b'))
    ipt_2 = 'a'
    exp_2 = (('a', ), )
    ipt_3 = 'abcbddbace'

    # assert FSM('abcba', '', ()).palindrome is True
    # assert FSM('abcda', '', ()).palindrome is False
    # assert FSM('', '', ()).palindrome is True
    # assert FSM('a', '', ()).palindrome is True
    # assert FSM('bb', '', ()).palindrome is True
    # assert FSM('ac', '', ()).palindrome is False

    pp = PalindromePartitioning()
    assert pp.solution(ipt_1) == exp_1
    assert pp.solution(ipt_2) == exp_2
    print(pp.solution(ipt_3))
