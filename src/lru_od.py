from collections import OrderedDict


class LRUCache:
    __slots__ = ('_limit', '_cache', '_count')

    def __init__(self, limit: int):
        self._limit = limit
        self._cache = OrderedDict()
        self._count = 0

    @property
    def full(self) -> bool:
        return self._count >= self._limit

    def __repr__(self):
        return repr(self._cache)

    def __str__(self):
        return self.__repr__()

    def _get(self, key) -> bool:
        return self._cache.get(key)

    def existing(self, key) -> bool:
        value = self._get(key)
        return not value is None

    def set(self, key, value):
        existing = self.existing(key)
        # update & move to end
        self._cache.update(**{key: value})
        if not existing and self.full:
            self._cache.popitem(last=False)
        if not existing and not self.full:
            self._count += 1

    def get(self, key):
        value = self._get(key)
        if not value is None:
            self._cache.move_to_end(key)
        return value


if __name__ == '__main__':
    lru = LRUCache(5)

    lru.set('c', 'ccc')
    lru.set('b', 'bbb')
    lru.set('a', 'aaa')
    lru.set(3, 333)
    lru.set(2, 222)
    lru.set(1, 111)

    print(lru)
    print(lru.get(3))
    print(lru)
