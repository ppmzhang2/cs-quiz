"""convert chinese characters to number"""
from dataclasses import dataclass
from enum import IntEnum, unique
from functools import reduce
from typing import List, Optional, Union


@unique
class Unit(IntEnum):
    """number unit"""
    GE = 1
    SHI = 10
    BAI = 100
    QIAN = 1000
    WAN = 10000
    YI = 100000000
    INF = 9999999999


_MAP_FROM_CH = {
    '零': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': Unit.SHI,
    '百': Unit.BAI,
    '千': Unit.QIAN,
    '万': Unit.WAN,
    '亿': Unit.YI,
}


@unique
class State(IntEnum):
    """converter states"""
    INVALID = 0
    MERGE_BASIC = 1
    MERGE_COMPOUND = 2
    FILL_BASIC_UNIT = 3
    FILL_BASIC_DIGIT = 4
    FILL_COMPOUND_UNIT = 5
    BEFORE_ENDING = 6
    DONE = 7


@dataclass(frozen=True)
class BasicStrNum:
    """character number with digit and unit"""
    digit: Optional[int]
    unit: Optional[Unit]

    @property
    def num(self) -> Optional[int]:
        """resulting number"""
        if self.digit is None or self.unit is None:
            return None
        return self.digit * self.unit.value


@dataclass(frozen=True)
class CompoundStrNum:
    """compound string number built with `BasicStrNum`"""
    addons: List[BasicStrNum]
    unit: Optional[Unit]

    @property
    def num(self) -> Optional[int]:
        """resulting number"""
        if self.unit is None:
            return None
        return (reduce(lambda x, y: x + y,
                       (addon.num for addon in self.addons)) * self.unit.value)


@dataclass
class FinalStrNum:
    """final string number build with `CompoundStrNum`"""
    addons: List[CompoundStrNum]

    @property
    def num(self) -> int:
        """resulting number"""
        return reduce(lambda x, y: x + y, (addon.num for addon in self.addons))


@dataclass(frozen=True)
class FSM:
    """converter FSM"""
    unit: Optional[Unit]
    basic: BasicStrNum
    compound: CompoundStrNum
    final: FinalStrNum
    chars: List[Union[int, Unit]]

    @property
    def head(self) -> Optional[Union[int, Unit]]:
        """head of chars"""
        if not self.chars:
            return None
        return self.chars[0]

    @property
    def rest(self) -> List[Union[int, Unit]]:
        """rest of chars"""
        if not self.chars:
            return []
        return self.chars[1:]

    @property
    def state(self) -> State:
        # pylint: disable=too-many-return-statements
        """converter state"""
        if self.head is None and self.basic.digit is not None:
            return State.BEFORE_ENDING
        if self.head is None:
            return State.DONE
        if isinstance(self.head, Unit) and self.head > self.unit:
            return State.FILL_COMPOUND_UNIT
        if self.compound.unit is not None:
            return State.MERGE_COMPOUND
        if (self.basic.digit is None and self.basic.unit is None
                and self.compound.unit is None):
            return State.FILL_BASIC_DIGIT
        if (self.basic.digit is not None and self.basic.unit is None
                and self.compound.unit is None):
            return State.FILL_BASIC_UNIT
        if self.basic.digit is not None and self.basic.unit is not None:
            return State.MERGE_BASIC
        raise ValueError('value error')

    @staticmethod
    def string_parse(ch: str) -> List[Union[int, Unit]]:
        """from chinese string to sequence of integer of units"""
        seq_ch = list(ch)
        # remove zero as it is only a placeholder
        return list(
            filter(lambda x: x != 0, [_MAP_FROM_CH.get(c) for c in seq_ch]))


class Converter:
    """converter functions"""
    @staticmethod
    def init_fsm(ch: str):
        """initiate FSM instance"""
        seq = FSM.string_parse(ch)
        return FSM(
            unit=Unit.INF,
            basic=BasicStrNum(digit=None, unit=None),
            compound=CompoundStrNum(addons=[], unit=None),
            final=FinalStrNum(addons=[]),
            chars=seq,
        )

    @staticmethod
    def transform(fsm: FSM):
        """transform FSM instance"""
        while True:
            if fsm.state == State.DONE:
                return fsm
            if fsm.state == State.BEFORE_ENDING:
                new_basic = BasicStrNum(
                    digit=fsm.basic.digit,
                    unit=(fsm.basic.unit or Unit.GE),
                )
                new_compound = CompoundStrNum(
                    addons=[*fsm.compound.addons, new_basic],
                    unit=Unit.GE,
                )
                fsm = FSM(
                    unit=None,
                    basic=BasicStrNum(digit=None, unit=None),
                    compound=CompoundStrNum(addons=[], unit=None),
                    final=FinalStrNum(
                        addons=[*fsm.final.addons, new_compound]),
                    chars=[],
                )
            elif fsm.state == State.FILL_BASIC_DIGIT:
                fsm = FSM(
                    unit=fsm.unit,
                    basic=BasicStrNum(digit=fsm.head, unit=fsm.basic.unit),
                    compound=fsm.compound,
                    final=fsm.final,
                    chars=fsm.rest,
                )
            elif fsm.state == State.FILL_BASIC_UNIT:
                fsm = FSM(
                    unit=fsm.head,
                    basic=BasicStrNum(digit=fsm.basic.digit, unit=fsm.head),
                    compound=fsm.compound,
                    final=fsm.final,
                    chars=fsm.rest,
                )
            elif fsm.state == State.MERGE_BASIC:
                fsm = FSM(
                    unit=fsm.unit,
                    basic=BasicStrNum(digit=None, unit=None),
                    compound=CompoundStrNum(
                        addons=[*fsm.compound.addons, fsm.basic],
                        unit=fsm.compound.unit,
                    ),
                    final=fsm.final,
                    chars=fsm.chars,
                )
            elif fsm.state == State.MERGE_COMPOUND:
                fsm = FSM(
                    unit=fsm.unit,
                    basic=fsm.basic,
                    compound=CompoundStrNum(
                        addons=[],
                        unit=None,
                    ),
                    final=FinalStrNum(
                        addons=[*fsm.final.addons, fsm.compound]),
                    chars=fsm.chars,
                )
            elif fsm.state == State.FILL_COMPOUND_UNIT:
                new_basic = BasicStrNum(fsm.basic.digit, unit=Unit.GE)
                fsm = FSM(
                    unit=Unit.INF,
                    basic=BasicStrNum(digit=None, unit=None),
                    compound=CompoundStrNum(
                        addons=[*fsm.compound.addons, new_basic],
                        unit=fsm.head,
                    ),
                    final=fsm.final,
                    chars=fsm.rest,
                )
            else:
                raise ValueError('state error')

    @classmethod
    def solution(cls, ch: str):
        """final solution"""
        fsm = cls.init_fsm(ch)
        return cls.transform(fsm).final.num


if __name__ == '__main__':
    input_1 = '五千六百八十七万三千四百二十九'
    exp_1 = 56873429
    input_2 = '九千九百九十九万九千九百九十'
    exp_2 = 99999990
    input_3 = '一千零三十四万五千零五十六'
    exp_3 = 10345056
    input_4 = '五十三亿七千二百六十五万四千八百三十九'
    exp_4 = 5372654839

    assert Converter.solution(input_1) == exp_1
    assert Converter.solution(input_2) == exp_2
    assert Converter.solution(input_3) == exp_3
    assert Converter.solution(input_4) == exp_4
