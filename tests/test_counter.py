import unittest

from counter import Counter


class TestCounter(unittest.TestCase):

    def test_default_value(self):
        counter = Counter()
        self.assertEqual(counter.value, 0)

    def test_reset(self):
        counter = Counter(1)
        counter.Reset()
        self.assertEqual(counter.value, 0)

    def test(self):
        self.counter = Counter()
        self.counter.Inc()
        self.assertEqual(self.counter(), 1, '')
        self.counter.Inc()
        self.assertEqual(self.counter(), 2, '')

    def test_convert_to_integer(self):
        self.assertEqual(int(Counter(3)), 3)

    def test_convert_to_string(self):
        self.assertEqual(str(Counter(4)), '4')

    def test_representation(self):
        self.assertEqual(repr(Counter(5)), 'Counter(5)')
