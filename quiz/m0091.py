"""Decode Ways
A message containing letters from A-Z can be encoded into numbers using the
following mapping:

'A' -> "1"
'B' -> "2"
...
'Z' -> "26"

To decode an encoded message, all the digits must be mapped back into letters
using the reverse of the mapping above (there may be multiple ways). For
example, "111" can have each of its "1"s be mapped into 'A's to make "AAA", or
it could be mapped to "11" and "1" ('K' and 'A' respectively) to make "KA".
Note that "06" cannot be mapped into 'F' since "6" is different from "06".

Given a non-empty string num containing only digits, return the number of ways
to decode it.

The answer is guaranteed to fit in a 32-bit integer.

Example 1:
Input: s = "12"
Output: 2
Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).

Example 2:
Input: s = "226"
Output: 3
Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or
"BBF" (2 2 6).

Example 3:
Input: s = "0"
Output: 0
Explanation: There is no character that is mapped to a number starting with 0.
The only valid mappings with 0 are 'J' -> "10" and 'T' -> "20".
Since there is no character, there are no valid ways to decode this since all
digits need to be mapped.

Example 4:
Input: s = "1"
Output: 1

Constraints:
* 1 <= s.length <= 100
* s contains only digits and may contain leading zero(s).
"""
from __future__ import annotations

from enum import Enum
from typing import NamedTuple, Optional, Sequence


class Code(Enum):
    A = '1'
    B = '2'
    C = '3'
    D = '4'
    E = '5'
    F = '6'
    G = '7'
    H = '8'
    I = '9'
    J = '10'
    K = '11'
    L = '12'
    M = '13'
    N = '14'
    O = '15'
    P = '16'
    Q = '17'
    R = '18'
    S = '19'
    T = '20'
    U = '21'
    V = '22'
    W = '23'
    X = '24'
    Y = '25'
    Z = '26'


class Status(Enum):
    DOING = 1
    ONE = 2
    DONE = 3
    INVALID = 4


class FSM(NamedTuple):
    ciphers: str
    codes: Sequence[Code]

    @property
    def remaining(self) -> int:
        return len(self.ciphers)

    @property
    def invalid(self):
        if len(list(filter(lambda x: x is None, self.codes))) >= 1:
            return True
        return False

    @property
    def status(self):
        if self.invalid:
            return Status.INVALID
        if self.remaining == 0:
            return Status.DONE
        if self.remaining == 1:
            return Status.ONE
        return Status.DOING


class Decode:
    @staticmethod
    def decipher(cipher: str) -> Optional[Code]:
        try:
            return Code(cipher)
        except ValueError:
            return None

    @classmethod
    def explode(cls, fsm: FSM) -> Sequence[FSM]:
        assert fsm.status in (Status.DOING, Status.ONE)

        if fsm.status == Status.ONE:
            return (FSM('', (*fsm.codes, cls.decipher(fsm.ciphers))), )

        splits = (
            (fsm.ciphers[1:], fsm.ciphers[:1]),
            (fsm.ciphers[2:], fsm.ciphers[:2]),
        )
        return tuple(
            FSM(tp[0], (*fsm.codes, cls.decipher(tp[1]))) for tp in splits)

    @classmethod
    def looper(cls, inputs: Sequence[FSM],
               outputs: Sequence[FSM]) -> Sequence[FSM]:
        if not inputs:
            return outputs
        fsm = inputs[0]
        if fsm.status == Status.INVALID:
            return cls.looper(inputs[1:], outputs)
        if fsm.status == Status.DONE:
            return cls.looper(inputs[1:], (*outputs, fsm))
        return cls.looper((*inputs[1:], *cls.explode(fsm)), outputs)

    def solution(self, text: str):
        fsm_seq = self.looper((FSM(text, ()), ), ())
        return len(fsm_seq)


if __name__ == '__main__':
    ipt_1 = '12'
    exp_1 = 2
    ipt_2 = '226'
    exp_2 = 3
    ipt_3 = '0'
    exp_3 = 0
    ipt_4 = '1'
    exp_4 = 1

    decode = Decode()

    # print(decode.explode(FSM(ipt_1, ())))

    assert decode.solution(ipt_1) == exp_1
    assert decode.solution(ipt_2) == exp_2
    assert decode.solution(ipt_3) == exp_3
    assert decode.solution(ipt_4) == exp_4
