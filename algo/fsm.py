"""FSM
if a string contains three or more groups of ascending characters with each
group has the same length, we call it a beautiful string (2014 MS)

* beautiful strings: abc, cde, aabbcc, aaabbbccc
* non-beautiful strings: abd, cba, aabbc, zab

input:

1. the first line is the number of cases
2. every line after the first line is a number and a string
3. the number is the length of the string, which is less than 10 MB

output: YES / NO

constains:

1. input only contains non-capital characters
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class AlphabetPhase(Enum):
    First = 1
    Middle = 2
    Last = 3
    Invalid = 4

    @property
    def is_last(self):
        return self == type(self).Last

    def next_phase(self) -> AlphabetPhase:
        assert not self.is_last
        if self == type(self).First:
            return type(self).Middle
        return type(self).Last


class Phase(Enum):
    First = 1
    Second = 2
    Third = 3
    Invalid = 4


class Status(Enum):
    First = 1
    Second = 2
    Third = 3
    Finished = 4
    Invalid = 5
    Restart = 6


@dataclass
class FSM:
    char: str
    first_phase_length: int
    second_phase_length: int
    third_phase_length: int
    remaining: str

    @property
    def phase(self) -> Phase:
        # how to set the FSM invalid
        if self.first_phase_length <= 0:
            return Phase.Invalid
        if self.second_phase_length == 0 and self.third_phase_length == 0:
            return Phase.First
        if self.third_phase_length == 0:
            return Phase.Second
        return Phase.Third

    @property
    def valid_length(self) -> str:
        # number of second character larger than the first one, invalid
        if self.second_phase_length > self.first_phase_length:
            return -1
        # in the first phase
        if self.phase == Phase.First:
            return self.first_phase_length
        # in the second phase
        if self.phase == Phase.Second:
            return self.second_phase_length
        # in the third phase
        if self.phase == Phase.Third:
            return self.second_phase_length

        raise ValueError('invalid value')

    @property
    def no_remaining(self) -> bool:
        return not self.remaining

    @property
    def invalid_char(self) -> bool:
        if self.no_remaining:
            return True
        char = self.remaining[0]
        if char not in (self.char, Solution.next_char(self.char)):
            return True

        return False

    @property
    def status(self) -> Status:
        if (self.phase == Phase.Third
                and self.third_phase_length == self.valid_length):
            return Status.Finished
        if (self.phase == Phase.First and not self.no_remaining
                and self.invalid_char):
            return Status.Restart
        if (self.phase == Phase.Invalid or self.valid_length == -1
                or self.invalid_char):
            return Status.Invalid
        if self.phase == Phase.First:
            return Status.First
        if self.phase == Phase.Second:
            return Status.Second
        if (self.phase == Phase.Third
                and self.third_phase_length < self.valid_length):
            return Status.Third

        raise ValueError('invalid value')

    def explode(self) -> Tuple[FSM, ...]:
        assert self.status in (
            Status.First,
            Status.Second,
            Status.Third,
            Status.Restart,
        )
        char = self.remaining[0]
        remaining = self.remaining[1:]
        if self.status == Status.Restart:
            return (FSM(char, 1, 0, 0, remaining), )
        if self.status == Status.First:
            if self.char == char:
                return (FSM(
                    self.char,
                    self.first_phase_length + 1,
                    self.second_phase_length,
                    self.third_phase_length,
                    remaining,
                ), )
            return (
                FSM(char, 1, 0, 0, remaining),
                FSM(
                    char,
                    self.first_phase_length,
                    self.second_phase_length + 1,
                    self.third_phase_length,
                    remaining,
                ),
            )
        if self.status == Status.Second:
            if self.char == char:
                return (FSM(
                    self.char,
                    self.first_phase_length,
                    self.second_phase_length + 1,
                    self.third_phase_length,
                    remaining,
                ), )
            return (
                FSM(char, 1, 0, 0, remaining),
                FSM(
                    char,
                    self.first_phase_length,
                    self.second_phase_length,
                    self.third_phase_length + 1,
                    remaining,
                ),
            )
        if self.status == Status.Third:
            if self.char == char:
                return (FSM(
                    self.char,
                    self.first_phase_length,
                    self.second_phase_length,
                    self.third_phase_length + 1,
                    remaining,
                ), )
            return (
                FSM(self.char, 1, 0, 0, remaining),
                FSM(self.char, self.second_phase_length, 1, 0, remaining),
                FSM(self.char, -1, 0, 0, remaining),
            )

        raise ValueError('invalid value')


class Solution:
    @staticmethod
    def next_char(c: str) -> str:
        ord_a = ord('a')

        def helper(n: int) -> int:
            return (n + 1 - ord_a) % 26 + ord_a

        if c in ('z', ''):
            return ''
        return chr(helper(ord(c)))

    @classmethod
    def looper(cls, inputs: Tuple[FSM, ...]) -> Optional[FSM]:
        if not inputs:
            return None
        fsm = inputs[0]
        if fsm.status == Status.Invalid:
            return cls.looper(inputs[1:])
        if fsm.status == Status.Finished:
            return fsm
        return cls.looper((*fsm.explode(), *inputs[1:]))

    def solution(self, string: str) -> bool:
        if len(string) == 0:
            return False
        char = string[0]
        remaining = string[1:]
        fsm_ = FSM(char, 1, 0, 0, remaining)
        res = self.looper((fsm_, ))
        if not res:
            return False
        return True


if __name__ == '__main__':
    ipt_1 = 'abc'
    exp_1 = True
    ipt_2 = 'cde'
    exp_2 = True
    ipt_3 = 'aaabbbccc'
    exp_3 = True
    ipt_4 = 'abd'
    exp_4 = False
    ipt_5 = 'cba'
    exp_5 = False
    ipt_6 = 'aabbc'
    exp_6 = False
    ipt_7 = 'zab'
    exp_7 = False
    ipt_8 = 'aaaaabbccc'
    exp_8 = True
    ipt_9 = 'fuiaabcsn'
    exp_9 = True

    s = Solution()

    assert s.next_char('b') == 'c'
    assert s.next_char('v') == 'w'
    assert s.next_char('z') == ''
    assert s.next_char('') == ''

    # phase = AlphabetPhase.First
    # print(phase.next_phase().is_last)
    # print(phase.next_phase().next_phase().is_last)

    # fsm = FSM('a', AlphabetPhase.First, 1, 0, 0, 'abbc')
    # print(fsm.explode()[0].explode()[1].explode()[0].explode())

    assert s.solution(ipt_1) == exp_1
    assert s.solution(ipt_2) == exp_2
    assert s.solution(ipt_3) == exp_3
    assert s.solution(ipt_4) == exp_4
    assert s.solution(ipt_5) == exp_5
    assert s.solution(ipt_6) == exp_6
    assert s.solution(ipt_7) == exp_7
    assert s.solution(ipt_8) == exp_8
    assert s.solution(ipt_9) == exp_9
