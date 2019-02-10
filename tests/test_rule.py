
import unittest

import rule as r


class TestRule(unittest.TestCase):

    def test_String(self):
        rule = r.Rule()
        self.assertEqual(str(rule), '3/23', 'Default rule string incorrect.')

        rule = r.Rule('12/23')
        self.assertEqual(str(rule), '12/23')

        rule = r.Rule('9876543210/')
        self.assertEqual(str(rule), '0123456789/')

        rule = r.Rule('/11')
        self.assertEqual(str(rule), '/1')

        rule = r.Rule('')
        self.assertEqual(str(rule), '/')

    def test_IsAliveNextGeneration(self):
        rule = r.Rule()

        self.assertTrue(rule.IsAliveNextGeneration(True, 3))
        self.assertTrue(rule.IsAliveNextGeneration(True, 2))
        self.assertTrue(rule.IsAliveNextGeneration(False, 3))

        self.assertFalse(rule.IsAliveNextGeneration(True, 4))
        self.assertFalse(rule.IsAliveNextGeneration(True, 1))
        self.assertFalse(rule.IsAliveNextGeneration(False, 4))
        self.assertFalse(rule.IsAliveNextGeneration(False, 2))

        rule = r.Rule('23/12')

        self.assertTrue(rule.IsAliveNextGeneration(True, 1))
        self.assertTrue(rule.IsAliveNextGeneration(True, 2))
        self.assertTrue(rule.IsAliveNextGeneration(False, 2))
        self.assertTrue(rule.IsAliveNextGeneration(False, 3))

        self.assertFalse(rule.IsAliveNextGeneration(True, 3))
        self.assertFalse(rule.IsAliveNextGeneration(True, 0))
        self.assertFalse(rule.IsAliveNextGeneration(False, 4))
        self.assertFalse(rule.IsAliveNextGeneration(False, 1))

    def test_born_and_survives(self):
        rule = r.Rule('3/23')
        self.assertEqual(rule.born, (3,))
        self.assertEqual(rule.survives, (2, 3))

        rule = r.Rule('12/23')
        self.assertEqual(rule.born, (1, 2))
        self.assertEqual(rule.survives, (2, 3))

        rule = r.Rule('23/12')
        self.assertEqual(rule.born, (2, 3))
        self.assertEqual(rule.survives, (1, 2))

        rule = r.Rule('9876543210/')
        self.assertEqual(rule.born, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(rule.survives, ())

        rule = r.Rule('/11')
        self.assertEqual(rule.born, ())
        self.assertEqual(rule.survives, (1,))

        rule = r.Rule('')
        self.assertEqual(rule.born, ())
        self.assertEqual(rule.survives, ())

    def test_StringToDigitTuple(self):
        self.assertEqual(r._StringToDigitTuple(''), ())
        self.assertEqual(
            r._StringToDigitTuple('jasdjf $ ;\\!"$%^//&*()\'#;[]\':{:\')'),
            ())
        self.assertEqual(
            r._StringToDigitTuple('93648261'),
            (1, 2, 3, 4, 6, 8, 9))
        self.assertEqual(
            r._StringToDigitTuple('djksd2kdfadfk3kfa;@~}1'),
            (1, 2, 3))
        self.assertEqual(
            r._StringToDigitTuple('11111111111111111111adjfa33333333jdfj5555'),
            (1, 3, 5))

    def test_RuleToString(self):
        self.assertEqual(r._RuleToString(((), ())), '/', 'empty')
        self.assertEqual(r._RuleToString(((1,), (2,))), '1/2', '1 by 1')
        self.assertEqual(r._RuleToString(((1, 2), (3,))), '12/3', '2 by 1')
        self.assertEqual(r._RuleToString(((1, 2), (3, 4))), '12/34', '2 by 2')
        self.assertEqual(r._RuleToString(((1,), (2,), (3,))), '1/2', '>2.')

    def test_StringToRule(self):
        self.assertEqual(r._StringToRule(), ((3,), (2, 3)), 'default')
        self.assertEqual(r._StringToRule(''), ((), ()), 'empty')
        self.assertEqual(r._StringToRule('/'), ((), ()), 'just separator')
        self.assertEqual(r._StringToRule('1/'), ((1,), ()), 'first empty')
        self.assertEqual(r._StringToRule('/2'), ((), (2,)), 'second empty')
        self.assertEqual(r._StringToRule('1/2'), ((1,), (2,)), '1 by 1.')
        self.assertEqual(
            r._StringToRule('  5  6  /  7  8  \r\n\t!"$%^&*()'),
            ((5, 6), (7, 8)),
            'ignore invalid characters')
        self.assertEqual(r._StringToRule('12/3'), ((1, 2), (3,)), '2 by 1')
        self.assertEqual(r._StringToRule('12/34'), ((1, 2), (3, 4)), '2 by 2')
        self.assertEqual(r._StringToRule('1/2/3'), ((1,), (2,)), '>2')

    def test_RuleParserFromString_GetRule_RuleToString(self):
        ruleStr = '45/89'
        rule = r.Rule(ruleStr)
        self.assertEqual(str(rule), ruleStr)
