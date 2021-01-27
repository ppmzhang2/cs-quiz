from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class BaseContext(Generic[T]):
    pass


@dataclass(frozen=True)
class BaseContexts:
    rec: BaseContexts

    @property
    def context(self):
        raise NotImplementedError

    @property
    def depth(self):
        def helper(rec, acc):
            if not rec:
                return acc
            return helper(rec.rec, acc + 1)

        if not self:
            return 0
        return helper(self.rec, 1)

    def _str(self):
        if not self:
            return repr(self)
        return repr(self.context) + '\n->\n' + type(self)._str(self.rec)

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self.__str__()


class BaseZipper(Generic[T]):
    @property
    def _body(self):
        raise NotImplementedError

    @property
    def _contexts(self) -> BaseContexts[T]:
        raise NotImplementedError

    @property
    def depth(self) -> int:
        return self._contexts.depth

    @property
    def top(self) -> bool:
        return self._contexts is None

    @property
    def bottom(self) -> bool:
        raise NotImplementedError

    def go_up(self) -> BaseZipper:
        raise NotImplementedError

    def go_down(self, *args, **kwargs) -> BaseZipper:
        raise NotImplementedError

    def go_up_most(self) -> BaseZipper:
        if self.top:
            return self
        return self.go_up().go_up_most()

    def go_down_most(self, *args, **kwargs) -> BaseZipper:
        raise NotImplementedError

    def __str__(self):
        return '\n'.join((
            f'body: {repr(self._body)}',
            f'contexts: {repr(self._contexts)}',
        ))
