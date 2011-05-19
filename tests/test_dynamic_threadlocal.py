#!/usr/bin/env python
import unittest
from dynamic_threadlocal import dynamic

class TestDynamic(unittest.TestCase):

    def test_all(self):
        self.assertFalse(dynamic._threadlocal.dynamic_frame)

        def foo():
            with dynamic(x=5) as d:
                return bar()

        def bar():
            return dynamic.x

        self.assertRaises(NameError, bar)

        with dynamic(x = 7) as d:
            self.assertEquals(bar(), 7)

            d.x = 8
            self.assertEquals(bar(), 8)

            self.assertEquals(foo(), 5)
            self.assertEquals(bar(), 8)

            del d.x
            self.assertRaises(NameError, bar)

        self.assertFalse(dynamic._threadlocal.dynamic_frame)

if __name__ == '__main__':
    unittest.main()
