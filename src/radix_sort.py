from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, NoReturn, Tuple

import pydantic


@dataclass(frozen=True)
class Radix:
    seq: Tuple[int, ...]

    def get(self, idx: int) -> int:
        try:
            return self.seq[idx]
        except IndexError:
            return 0

    @property
    def num(self):
        return int(''.join(map(str, reversed(self.seq))))


class FSM(pydantic.BaseModel):
    radices: Tuple[Radix, ...]
    idx: int
    dc: DefaultDict[int, list] = defaultdict(list)

    @property
    def done(self) -> bool:
        return not self.radices

    @property
    def ordered(self) -> Tuple[Radix, ...]:
        return tuple(v for key in sorted(self.dc.keys()) for v in self.dc[key])

    @property
    def nums(self) -> Tuple[int, ...]:
        return tuple(radix.num for radix in self.radices)

    def transform(self) -> NoReturn:
        for radix in self.radices:
            self.dc[radix.get(self.idx)].append(radix)
        self.radices = ()

    def rotate(self) -> NoReturn:
        self.radices = self.ordered
        self.idx += 1
        self.dc = defaultdict(list)


class RadixSort:
    @staticmethod
    def num_to_radix(num: int) -> Radix:
        return Radix(tuple(map(int, reversed(str(num)))))

    def solution(self, seq: Tuple[int, ...], limit: int):
        radices = tuple(self.num_to_radix(n) for n in seq)
        fsm = FSM(radices=radices, idx=0)
        while True:
            if fsm.idx >= limit - 1:
                return fsm.nums
            if fsm.done:
                fsm.rotate()
            else:
                fsm.transform()


if __name__ == '__main__':
    ipt_1_1 = (2, 4, 6, 0, 1, 9, 3, 8, 5, 7)
    ipt_1_2 = 3
    exp_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    rs = RadixSort()

    # num_1 = 24601
    # print(rs.num_to_radix(num_1).num)
    # print(rs.num_to_radix(num_1).get(6))

    assert exp_1 == rs.solution(ipt_1_1, ipt_1_2)
