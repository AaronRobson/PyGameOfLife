import unittest

import counter


class TestCounter(unittest.TestCase):

    def setUp(self):
        self.support = counter
        self.widget = self.support.Counter()

    def test(self):
        self.assertEqual(self.widget(), 0, '')
        self.widget.Inc()
        self.assertEqual(self.widget(), 1, '')
        self.widget.Inc()
        self.assertEqual(self.widget(), 2, '')

        self.assertEqual(int(self.widget), 2, '')
        self.assertEqual('%d' % (self.widget), '2', '')
        self.assertEqual('%s' % (self.widget), '2', '')

        self.widget.Reset()
        self.assertEqual(self.widget(), 0, '')


if __name__ == "__main__":
    unittest.main()
