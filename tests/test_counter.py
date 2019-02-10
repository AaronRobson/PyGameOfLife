import unittest

from counter import Counter


class TestCounter(unittest.TestCase):

    def setUp(self):
        self.counter = Counter()

    def test(self):
        self.assertEqual(self.counter(), 0, '')
        self.counter.Inc()
        self.assertEqual(self.counter(), 1, '')
        self.counter.Inc()
        self.assertEqual(self.counter(), 2, '')

        self.assertEqual(int(self.counter), 2, '')
        self.assertEqual('%d' % (self.counter), '2', '')

        self.counter.Reset()
        self.assertEqual(self.counter(), 0, '')

    def test_convert_to_string(self):
        self.assertEqual(str(Counter(4)), '4')

    def test_representation(self):
        self.assertEqual(repr(Counter(5)), 'Counter(5)')
