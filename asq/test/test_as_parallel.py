import sys
import unittest
from asq.queryables import Queryable

__author__ = "Robert Smallshire"

if not sys.platform == 'cli':

    class TestAsParallel(unittest.TestCase):

        def test_as_parallel_closed(self):
            b = Queryable([1])
            b.close()
            self.assertRaises(ValueError, lambda: b.as_parallel())