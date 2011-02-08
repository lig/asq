import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'

class TestSkipWhile(unittest.TestCase):

    def test_skip_while(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).skip_while(lambda x: x < 'e').to_list()
        c = ['e', 'f', 'g']
        self.assertEqual(b, c)

    def test_skip_while_from_infinite(self):
        b = Queryable(infinite()).skip_while(lambda x: x < 5).take(3).to_list()
        c = [5, 6, 7]
        self.assertEqual(b, c)

    def test_skip_while_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).skip_while(lambda x: x < 3)
        self.assertEqual(a.trace, [])
        c = b.take(3).to_list()
        # 3 is included here in the trace because it must have been consumed in order to test
        # whether it satisfies the predicate
        self.assertEqual(a.trace, [0, 1, 2, 3, 4, 5])

  