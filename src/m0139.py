"""Word Break
Given a non-empty string s and a dictionary wordDict containing a list of
non-empty words, determine if s can be segmented into a space-separated
sequence of one or more dictionary words.

Note:
The same word in the dictionary may be reused multiple times in the
segmentation.

You may assume the dictionary does not contain duplicate words.

Example 1:
Input: s = "leetcode", wordDict = ["leet", "code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".

Example 2:
Input: s = "applepenapple", wordDict = ["apple", "pen"]
Output: true
Explanation: Return true because "applepenapple" can be segmented as "apple pen
  apple". Note that you are allowed to reuse a dictionary word.

Example 3:
Input: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
Output: false
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Tuple


@unique
class State(IntEnum):
    TO_EXPLODE = 1
    TO_TRANSFER = 2
    INVALID = 3
    DONE = 4


@dataclass(frozen=True)
class FSM:
    dictionary: Tuple[str, ...]
    index: Optional[int]
    string: str
    words: Tuple[str, ...]

    @property
    def focusing_word(self) -> Optional[str]:
        if self.index is None:
            return None
        return self.dictionary[self.index]

    @property
    def invalid(self) -> bool:
        if self.index is None:
            return False
        try:
            pattern = self.string[:len(self.focusing_word)]
            if self.focusing_word != pattern:
                return True
            return False
        except IndexError:
            return True

    @property
    def state(self) -> State:
        if not self.string:
            return State.DONE
        if self.index is None:
            return State.TO_EXPLODE
        if self.invalid:
            return State.INVALID
        return State.TO_TRANSFER

    def explode(self) -> Tuple[FSM, ...]:
        return tuple(
            FSM(
                self.dictionary,
                idx,
                self.string,
                self.words,
            ) for idx, _ in enumerate(self.dictionary))

    def transfer(self) -> FSM:
        return FSM(
            self.dictionary,
            None,
            self.string[len(self.focusing_word):],
            (*self.words, self.focusing_word),
        )

    def transform(self) -> Tuple[FSM, ...]:
        if self.state == State.TO_EXPLODE:
            return self.explode()
        if self.state == State.TO_TRANSFER:
            return (self.transfer(), )
        raise ValueError('invalid FSM')


class WordBreak:
    @staticmethod
    def looper(inputs: Tuple[FSM, ...], outputs: Tuple[Tuple[str, ...], ...]):
        while True:
            if not inputs:
                return outputs
            fsm = inputs[0]
            if fsm.state == State.DONE:
                inputs, outputs = inputs[1:], (*outputs, fsm.words)
            elif fsm.state == State.INVALID:
                inputs = inputs[1:]
            else:
                inputs = (*fsm.transform(), *inputs[1:])

    def solution(self, string: str,
                 dictionary: Tuple[str, ...]) -> Tuple[Tuple[str, ...], ...]:
        fsm = FSM(dictionary, None, string, ())
        return tuple(sorted(self.looper((fsm, ), ())))


if __name__ == '__main__':
    ipt_1_1 = 'leetcode'
    ipt_1_2 = ('leet', 'code')
    exp_1 = (('leet', 'code'), )
    ipt_2_1 = 'applepenapple'
    ipt_2_2 = ('apple', 'pen')
    exp_2 = (('apple', 'pen', 'apple'), )
    ipt_3_1 = 'catsandog'
    ipt_3_2 = ('cats', 'dog', 'sand', 'and', 'cat')
    exp_3 = ()
    ipt_4_1 = 'catsanddog'
    ipt_4_2 = ('cats', 'dog', 'sand', 'and', 'cat')
    exp_4 = (('cat', 'sand', 'dog'), ('cats', 'and', 'dog'))

    wb = WordBreak()
    assert wb.solution(ipt_1_1, ipt_1_2) == exp_1
    assert wb.solution(ipt_2_1, ipt_2_2) == exp_2
    assert wb.solution(ipt_3_1, ipt_3_2) == exp_3
    assert wb.solution(ipt_4_1, ipt_4_2) == exp_4
