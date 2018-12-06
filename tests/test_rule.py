
import unittest

import rule


class TestRule(unittest.TestCase):
    def setUp(self):
        self.support = rule
        self.widget = self.support.Rule

    def test_String(self):
        rule = self.widget()
        self.assertEqual(str(rule), '3/23', 'Default rule string incorrect.')

        rule = self.widget('12/23')
        self.assertEqual(str(rule), '12/23', '')

        rule = self.widget('9876543210/')
        self.assertEqual(str(rule), '0123456789/', '')

        rule = self.widget('/11')
        self.assertEqual(str(rule), '/1', '')

        rule = self.widget('')
        self.assertEqual(str(rule), '/', '')

    def test_IsAliveNextGeneration(self):
        rule = self.widget()

        self.assertTrue(rule.IsAliveNextGeneration(True, 3), '')
        self.assertTrue(rule.IsAliveNextGeneration(True, 2), '')
        self.assertTrue(rule.IsAliveNextGeneration(False, 3), '')

        self.assertFalse(rule.IsAliveNextGeneration(True, 4), '')
        self.assertFalse(rule.IsAliveNextGeneration(True, 1), '')
        self.assertFalse(rule.IsAliveNextGeneration(False, 4), '')
        self.assertFalse(rule.IsAliveNextGeneration(False, 2), '')

        rule = self.widget('23/12')

        self.assertTrue(rule.IsAliveNextGeneration(True, 1), '')
        self.assertTrue(rule.IsAliveNextGeneration(True, 2), '')
        self.assertTrue(rule.IsAliveNextGeneration(False, 2), '')
        self.assertTrue(rule.IsAliveNextGeneration(False, 3), '')

        self.assertFalse(rule.IsAliveNextGeneration(True, 3), '')
        self.assertFalse(rule.IsAliveNextGeneration(True, 0), '')
        self.assertFalse(rule.IsAliveNextGeneration(False, 4), '')
        self.assertFalse(rule.IsAliveNextGeneration(False, 1), '')

    def test_born_and_survives(self):
        rule = self.widget('3/23')
        self.assertEqual(rule.born, (3,), '')
        self.assertEqual(rule.survives, (2, 3), '')

        rule = self.widget('12/23')
        self.assertEqual(rule.born, (1, 2), '')
        self.assertEqual(rule.survives, (2, 3), '')

        rule = self.widget('23/12')
        self.assertEqual(rule.born, (2, 3), '')
        self.assertEqual(rule.survives, (1, 2), '')

        rule = self.widget('9876543210/')
        self.assertEqual(rule.born, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), '')
        self.assertEqual(rule.survives, (), '')

        rule = self.widget('/11')
        self.assertEqual(rule.born, (), '')
        self.assertEqual(rule.survives, (1,), '')

        rule = self.widget('')
        self.assertEqual(rule.born, (), '')
        self.assertEqual(rule.survives, (), '')

    def test_StringToDigitTuple(self):
        self.assertEqual(self.support._StringToDigitTuple(''), (), '')
        self.assertEqual(self.support._StringToDigitTuple('jasdjf $ ;\!"$%^//&*()\'#;[]\':{:\')'), (), '')
        self.assertEqual(self.support._StringToDigitTuple('93648261'), (1, 2, 3, 4, 6, 8, 9), '')
        self.assertEqual(self.support._StringToDigitTuple('djksd2kdfadfk3kfa;@~}1'), (1, 2, 3), '')
        self.assertEqual(self.support._StringToDigitTuple('11111111111111111111adjfa33333333jdfj5555'), (1, 3, 5), '')

    def test_RuleToString(self):
        self.assertEqual(self.support._RuleToString(((), ())), '/', 'RuleToString Fail: on empty notation.')
        self.assertEqual(self.support._RuleToString(((1,), (2,))), '1/2', 'RuleToString Fail: on standard notation 1 by 1.')
        self.assertEqual(self.support._RuleToString(((1, 2), (3,))), '12/3', 'RuleToString Fail: on standard notation 2 by 1.')
        self.assertEqual(self.support._RuleToString(((1, 2), (3, 4))), '12/34', 'RuleToString Fail: on standard notation extended 2 by 2.')
        self.assertEqual(self.support._RuleToString(((1,), (2,), (3,))), '1/2', 'RuleToString Fail: on more than two rule sections.')

    def test_StringToRule(self):
        self.assertEqual(self.support._StringToRule(), ((3,), (2, 3)), 'StringToRule Fail: default rule incorrect.')
        self.assertEqual(self.support._StringToRule(''), ((), ()), 'StringToRule Fail: on empty notation.')
        self.assertEqual(self.support._StringToRule('/'), ((), ()), 'StringToRule Fail: on only separator notation.')
        self.assertEqual(self.support._StringToRule('1/'), ((1,), ()), 'StringToRule Fail: on first empty.')
        self.assertEqual(self.support._StringToRule('/2'), ((), (2,)), 'StringToRule Fail: on second empty.')
        self.assertEqual(self.support._StringToRule('1/2'), ((1,), (2,)), 'StringToRule Fail: on standard notation 1 by 1.')
        self.assertEqual(self.support._StringToRule('  5  6  /  7  8  \r\n\t!"$%^&*()'), ((5, 6), (7, 8)), 'StringToRule Fail: Fails to ignore whitespace and other characters properly.')
        self.assertEqual(self.support._StringToRule('12/3'), ((1, 2), (3,)), 'StringToRule Fail: on standard notation 2 by 1.')
        self.assertEqual(self.support._StringToRule('12/34'), ((1, 2), (3, 4)), 'StringToRule Fail: on standard notation extended 2 by 2.')
        self.assertEqual(self.support._StringToRule('1/2/3'), ((1,), (2,)), 'StringToRule Fail: on more than two rule sections.')

    def test_RuleParserFromString_GetRule_RuleToString(self):
        ruleStr = '45/89'
        rule = self.widget(ruleStr)
        self.assertEqual(str(rule), ruleStr, 'RuleParserFromString & GetRule & RuleToString Fail: custom 2 by 2 rule round trip change.')


if __name__ == "__main__":
    unittest.main()
