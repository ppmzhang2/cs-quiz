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
from enum import Enum, unique
from typing import Optional, Tuple


@unique
class Phase(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    INVALID = 4


@unique
class Status(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    DONE = 4
    INVALID = 5
    RESTART = 6


@dataclass(frozen=True)
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
            return Phase.INVALID
        if self.second_phase_length == 0 and self.third_phase_length == 0:
            return Phase.FIRST
        if self.third_phase_length == 0:
            return Phase.SECOND
        return Phase.THIRD

    @property
    def valid_length(self) -> str:
        # number of second character larger than the first one, invalid
        if self.second_phase_length > self.first_phase_length:
            return -1
        # in the first phase
        if self.phase == Phase.FIRST:
            return self.first_phase_length
        # in the second phase
        if self.phase == Phase.SECOND:
            return self.second_phase_length
        # in the third phase
        if self.phase == Phase.THIRD:
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
        if char not in (self.char, BeautifulString.next_char(self.char)):
            return True

        return False

    @property
    def status(self) -> Status:
        if (self.phase == Phase.THIRD
                and self.third_phase_length == self.valid_length):
            return Status.DONE
        if (self.phase == Phase.FIRST and not self.no_remaining
                and self.invalid_char):
            return Status.RESTART
        if (self.phase == Phase.INVALID or self.valid_length == -1
                or self.invalid_char):
            return Status.INVALID
        if self.phase == Phase.FIRST:
            return Status.FIRST
        if self.phase == Phase.SECOND:
            return Status.SECOND
        if (self.phase == Phase.THIRD
                and self.third_phase_length < self.valid_length):
            return Status.THIRD

        raise ValueError('invalid value')

    def explode(self) -> Tuple[FSM, ...]:  #pylint: disable=too-many-return-statements
        assert self.status in (
            Status.FIRST,
            Status.SECOND,
            Status.THIRD,
            Status.RESTART,
        )
        char = self.remaining[0]
        remaining = self.remaining[1:]
        if self.status == Status.RESTART:
            return (FSM(char, 1, 0, 0, remaining), )
        if self.status == Status.FIRST:
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
        if self.status == Status.SECOND:
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
        if self.status == Status.THIRD:
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


class BeautifulString:
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
        if fsm.status == Status.INVALID:
            return cls.looper(inputs[1:])
        if fsm.status == Status.DONE:
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

    bs = BeautifulString()

    assert bs.next_char('b') == 'c'
    assert bs.next_char('v') == 'w'
    assert bs.next_char('z') == ''
    assert bs.next_char('') == ''

    assert bs.solution(ipt_1) == exp_1
    assert bs.solution(ipt_2) == exp_2
    assert bs.solution(ipt_3) == exp_3
    assert bs.solution(ipt_4) == exp_4
    assert bs.solution(ipt_5) == exp_5
    assert bs.solution(ipt_6) == exp_6
    assert bs.solution(ipt_7) == exp_7
    assert bs.solution(ipt_8) == exp_8
    assert bs.solution(ipt_9) == exp_9
