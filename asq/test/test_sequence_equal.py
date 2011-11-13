import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite

__author__ = "Robert Smallshire"

class TestSequenceEqual(unittest.TestCase):

    def test_sequence_equal_positive(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a).sequence_equal(b)
        self.assertTrue(c)

    def test_sequence_equal_negative(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 5, 16, 32)
        c = Queryable(a).sequence_equal(b)
        self.assertFalse(c)

    def test_sequence_equal_shorter_longer(self):
        a = [1, 2, 3]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a).sequence_equal(b)
        self.assertFalse(c)

    def test_sequence_equal_longer_shorter(self):
         a = [1, 2, 3, 4, 5, 6]
         b = (1, 2, 3)
         c = Queryable(a).sequence_equal(b)
         self.assertFalse(c)

    def test_sequence_equal_empty(self):
        a = []
        b = ()
        c = Queryable(a).sequence_equal(b)
        self.assertTrue(c)

    def test_sequence_equal_non_iterable(self):
        a = [1, 2, 3]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).sequence_equal(b))

    def test_sequence_equal_comparer(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (-1, 2, -3, 4, -16, 32)
        c = Queryable(a).sequence_equal(b, lambda a, b: abs(a) == abs(b))
        self.assertTrue(c)

    def test_sequence_equal_order(self):
        a = [1, 2]
        b = (2, 1)
        c = Queryable(a).sequence_equal(b)
        self.assertFalse(c)

    def test_sequence_equal_finite_infinite(self):
        a = infinite()
        b = (1, 2, 3, 5, 16, 32)
        c = Queryable(a).sequence_equal(b)
        self.assertFalse(c)

    def test_sequence_equal_infinite_finite(self):
        a = (1, 2, 3, 5, 16, 32)
        b = infinite()
        c = Queryable(a).sequence_equal(b)
        self.assertFalse(c)

    def test_sequence_equal_equality_comparer_positive(self):
        a = [1, 2, -3, 4, 16, 32]
        b = (-1, 2, 3, -4, 16, -32)
        c = Queryable(a).sequence_equal(b, lambda lhs, rhs: abs(lhs) == abs(rhs))
        self.assertTrue(c)

    def test_sequence_equal_equality_comparer_negative(self):
        a = [1, 2, -3, 4, 16, 32]
        b = (-1, 2, 3, -5, 16, -32)
        c = Queryable(a).sequence_equal(b, lambda lhs, rhs: abs(lhs) == abs(rhs))
        self.assertFalse(c)

    def test_sequence_equal_equality_comparer_not_callable(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 4, 16, 32)
        self.assertRaises(TypeError, lambda: Queryable(a).sequence_equal(b, "not callable"))
        
    def test_sequence_equal_closed(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a)
        c.close()
        self.assertRaises(ValueError, lambda: c.sequence_equal(b))



