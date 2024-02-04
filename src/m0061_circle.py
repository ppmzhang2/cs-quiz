"""Rotate List with Circle

1. Make the list circular
   - i.e. connect the last node to the first node
   - Also, count the number of nodes in the list (`L`)
2. Break the list at `k`-th node

Initial list:

    +===========+      +===========+                 +===========+
    |           |  +-->|           |  +-->       +-->|           |  +--> NULL
    +-----------+  |   +-----------+  |          |   +-----------+  |
    | value = 1 |  |   | value = 2 |  |    ...   |   | value = L |  |
    +-----------+  |   +-----------+  |          |   +-----------+  |
    |     p     |--+   |     p     |--+        --+   |     p     |--+
    +-----------+      +-----------+                 +-----------+

Make it circular:

      +===========+      +===========+                 +===========+
 +--> |           |  +-->|           |  +-->       +-->|           |
 |    +-----------+  |   +-----------+  |          |   +-----------+
 |    | value = 1 |  |   | value = 2 |  |    ...   |   | value = L |
 |    +-----------+  |   +-----------+  |          |   +-----------+
 |    |     p     |--+   |     p     |--+        --+   |     p     |--+
 |    +-----------+      +-----------+                 +-----------+  |
 |                                                                    |
 +--------------------------------------------------------------------+

Break the list at `k`-th node:

           +===========+            +===========+       +===========+
      +--> |           |  +--> NULL |           |  +--> |           |  +--> ...
      |    +-----------+  |         +-----------+  |    +-----------+  |
      |    | value = k |  |         |value = k+1|  |    |value = k+2|  |
...   |    +-----------+  |         +-----------+  |    +-----------+  |
      |    |     p     |--+         |     p     |--+    |     p     |--+
    --+    +-----------+            +-----------+       +-----------+

Re-order the list:

    +===========+      +===========+                 +===========+
    |           |  +-->|           |  +-->       +-->|           |  +--> NULL
    +-----------+  |   +-----------+  |          |   +-----------+  |
    |value = k+1|  |   |value = k+2|  |    ...   |   | value = k |  |
    +-----------+  |   +-----------+  |          |   +-----------+  |
    |     p     |--+   |     p     |--+        --+   |     p     |--+
    +-----------+      +-----------+                 +-----------+

Note: use `k % L` to avoid unnecessary rotations
"""
from __future__ import annotations


class Node:

    def __init__(self, data: int, next: Node = None):
        self._data = data
        self._next = next

    def next(self) -> Node:
        return self._next


class LinkedList:

    def __init__(self, head: Node):
        self._head = head

    def __str__(self):
        s = ""
        current = self._head
        while True:
            s += str(current._data)
            s += " -> "
            current = current.next()
            if current is None:
                return s + "None"

    def prepend(self, data: int):
        self._head = Node(data, self._head)

    def rotate(self, k: int):
        # 1. Traverse the list
        #    - find the length of the list
        #    - find the last node
        #    - make the list circular
        length = 1
        posledniy = self._head
        while True:
            if posledniy.next() is None:
                break
            length += 1
            posledniy = posledniy.next()
        posledniy._next = self._head
        # 2. break the circle at `k % length`
        break_at = k % length
        for _ in range(break_at):
            # posledniy still points to the last node, keep updating it
            posledniy = posledniy.next()
        self._head = posledniy.next()
        posledniy._next = None


if __name__ == "__main__":
    ll = LinkedList(Node(9))
    ll.prepend(8)
    ll.prepend(7)
    ll.prepend(6)
    ll.prepend(5)
    ll.prepend(4)
    ll.prepend(3)
    ll.prepend(2)
    ll.prepend(1)
    ll.prepend(0)
    str_rotate_1 = "1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 0 -> None"
    ll.rotate(1001)
    assert str(ll) == str_rotate_1
