"""group anagrams
Given an array of strings strs, group the anagrams together. You can return the
answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different
word or phrase, typically using all the original letters exactly once.

Example 1:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
Input: strs = [""]
Output: [[""]]

Example 3:
Input: strs = ["a"]
Output: [["a"]]

Constraints:
* 1 <= strs.length <= 10^4
* 0 <= strs[i].length <= 100
* strs[i] consists of lower-case English letters.
"""
from collections import defaultdict
from typing import DefaultDict, NamedTuple, Sequence, Tuple


class Middleware(NamedTuple):
    array: Tuple[str, ...]
    word: str


class Anagram:
    @staticmethod
    def add_id(word: str) -> Middleware:
        return Middleware(tuple(sorted(word)), word)

    @staticmethod
    def ingest(mws: Sequence[Middleware]) -> DefaultDict:
        dd = defaultdict(set)
        for _, mw in enumerate(mws):
            dd[mw.array].add(mw.word)

        return dd

    def solution(self, strs: Sequence[str]) -> Sequence[Sequence[str]]:
        mw_seq = tuple(self.add_id(word) for word in strs)
        dd = self.ingest(mw_seq)
        return tuple(sorted(tuple(sorted(t[1])) for t in dd.items()))


if __name__ == '__main__':
    ipt_1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    opt_1 = (
        ("ate", "eat", "tea"),
        ("bat", ),
        ("nat", "tan"),
    )
    ipt_2 = [""]
    opt_2 = (("", ), )
    ipt_3 = ["a"]
    opt_3 = (("a", ), )

    anagram = Anagram()

    assert anagram.add_id("eat") == Middleware(('a', 'e', 't'), 'eat')
    assert anagram.solution(ipt_1) == opt_1
    assert anagram.solution(ipt_2) == opt_2
    assert anagram.solution(ipt_3) == opt_3
