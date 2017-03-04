import unittest
import sunnydi


class MyTest(unittest.TestCase):

    def test_something(self):
        s = sunnydi.my_method()
        self.assertEquals(s, 'hi')
