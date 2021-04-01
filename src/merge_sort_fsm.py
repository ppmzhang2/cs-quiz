from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple


class MsArray(tuple):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args, **kwargs)

    def ordered_merge(self, arr: MsArray) -> MsArray:
        def helper(lhs: MsArray, rhs: MsArray, acc: MsArray) -> MsArray:
            while True:
                l_lhs = len(lhs)
                l_rhs = len(rhs)
                if not l_lhs and not l_rhs:
                    return acc
                if not lhs:
                    return MsArray(*acc, *rhs)
                if not rhs:
                    return MsArray(*acc, *lhs)
                i_lhs = lhs[0]
                i_rhs = rhs[0]
                if i_lhs <= i_rhs:
                    lhs, acc = lhs[1:], MsArray(*acc, i_lhs)
                else:
                    rhs, acc = rhs[1:], MsArray(*acc, i_rhs)

        return helper(self, arr, MsArray())


@dataclass(frozen=True)
class FSM:
    seq: Tuple[MsArray, ...]

    @property
    def length(self) -> int:
        return len(self.seq)

    @property
    def last(self) -> MsArray:
        return self.seq[-1]

    def merge(self) -> FSM:
        try:
            lhs, rhs = self.seq[:2]
        except ValueError:
            return self
        new_seq = self.seq[2:]
        new_arr = lhs.ordered_merge(rhs)
        return FSM((*new_seq, new_arr))


class MergeSort:
    @staticmethod
    def solution(seq: Sequence[int]):
        fsm = FSM(tuple(map(MsArray, seq)))
        while True:
            if fsm.length == 1:
                return fsm.last
            fsm = fsm.merge()


if __name__ == '__main__':
    ipt_1 = (2, 4, 6, 0, 1, 9, 3, 8, 5, 7)
    exp_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    # msa_1 = MsArray(2, 4, 6, 8)
    # msa_2 = MsArray(1, 3, 5, 7)

    ms = MergeSort()
    assert exp_1 == ms.solution(ipt_1)
