"""test for adt.stack

"""

import unittest

from adt.stack import Stack


class StackTest(unittest.TestCase):
    def test_str(self):
        stk1 = Stack()
        stk2 = Stack((1, ))
        stk3 = Stack(iter(['a', 'b', 'c']))
        stk1_str = 'Stack([])'
        stk2_str = 'Stack([1])'
        stk3_str = 'Stack([a, b, c])'
        self.assertEqual(str(stk1), stk1_str)
        self.assertEqual(str(stk2), stk2_str)
        self.assertEqual(str(stk3), stk3_str)

    def test_len(self):
        stk1 = Stack()
        stk2 = Stack((1, ))
        stk3 = Stack(iter(['a', 'b', 'c']))
        stk1_len = 0
        stk2_len = 1
        stk3_len = 3
        self.assertEqual(len(stk1), stk1_len)
        self.assertEqual(len(stk2), stk2_len)
        self.assertEqual(len(stk3), stk3_len)

    def test_peak(self):
        stk1 = Stack()
        stk2 = Stack((1, ))
        stk3 = Stack(iter(['a', 'b', 'c']))
        stk2_peak = 1
        stk3_peak = 'c'
        self.assertRaises(Exception, stk1.peak)
        self.assertEqual(stk2.peak(), stk2_peak)
        self.assertEqual(stk3.peak(), stk3_peak)

    def test_action(self):
        stk = Stack(iter(['a', 'b', 'c']))
        stk_str1 = 'Stack([a, b, c])'
        stk_str2 = 'Stack([a, b, d, e])'
        self.assertEqual(str(stk), stk_str1)
        stk.pop()
        stk.push('d')
        stk.push('e')
        self.assertEqual(str(stk), stk_str2)

    def test_iter(self):
        stk1 = Stack()
        stk2 = Stack((1, ))
        stk3 = Stack(iter(['a', 'b', 'c']))
        stk1_iter = []
        stk2_iter = [1]
        stk3_iter = ['c', 'b', 'a']
        self.assertEqual(list(iter(stk1)), stk1_iter)
        self.assertEqual(list(iter(stk2)), stk2_iter)
        self.assertEqual(list(iter(stk3)), stk3_iter)
        self.assertEqual(True, stk1.empty())
        self.assertEqual(True, stk2.empty())
        self.assertEqual(True, stk3.empty())


if __name__ == '__main__':
    unittest.main(verbosity=2)
