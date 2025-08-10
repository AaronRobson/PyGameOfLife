import unittest
from unittest.mock import patch

import rule as r


class TestRule(unittest.TestCase):

    def test_representation(self):
        rule = r.Rule('1/2')
        self.assertEqual(repr(rule), "Rule('1/2')")

    def test_text(self):
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

    def test_is_alive_next_generation(self):
        rule = r.Rule()

        self.assertTrue(rule.is_alive_next_generation(True, 3))
        self.assertTrue(rule.is_alive_next_generation(True, 2))
        self.assertTrue(rule.is_alive_next_generation(False, 3))

        self.assertFalse(rule.is_alive_next_generation(True, 4))
        self.assertFalse(rule.is_alive_next_generation(True, 1))
        self.assertFalse(rule.is_alive_next_generation(False, 4))
        self.assertFalse(rule.is_alive_next_generation(False, 2))

        rule = r.Rule('23/12')

        self.assertTrue(rule.is_alive_next_generation(True, 1))
        self.assertTrue(rule.is_alive_next_generation(True, 2))
        self.assertTrue(rule.is_alive_next_generation(False, 2))
        self.assertTrue(rule.is_alive_next_generation(False, 3))

        self.assertFalse(rule.is_alive_next_generation(True, 3))
        self.assertFalse(rule.is_alive_next_generation(True, 0))
        self.assertFalse(rule.is_alive_next_generation(False, 4))
        self.assertFalse(rule.is_alive_next_generation(False, 1))

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

    def test_string_to_digit_tuple(self):
        self.assertEqual(r._string_to_digit_tuple(''), ())
        self.assertEqual(
            r._string_to_digit_tuple('jasdjf $ ;\\!"$%^//&*()\'#;[]\':{:\')'),
            ())
        self.assertEqual(
            r._string_to_digit_tuple('93648261'),
            (1, 2, 3, 4, 6, 8, 9))
        self.assertEqual(
            r._string_to_digit_tuple('djksd2kdfadfk3kfa;@~}1'),
            (1, 2, 3))
        self.assertEqual(
            r._string_to_digit_tuple('1111111111111111adjfa33333333jdfj5555'),
            (1, 3, 5))

    def test_rule_to_string(self):
        self.assertEqual(r._rule_to_string(((), ())), '/', 'empty')
        self.assertEqual(r._rule_to_string(((1,), (2,))), '1/2', '1 by 1')
        self.assertEqual(r._rule_to_string(((1, 2), (3,))), '12/3', '2 by 1')
        self.assertEqual(
            r._rule_to_string(((1, 2), (3, 4))), '12/34',
            '2 by 2')
        self.assertEqual(r._rule_to_string(((1,), (2,), (3,))), '1/2', '>2.')

    def test_string_to_rule(self):
        self.assertEqual(r._string_to_rule(), ((3,), (2, 3)), 'default')
        self.assertEqual(r._string_to_rule(''), ((), ()), 'empty')
        self.assertEqual(r._string_to_rule('/'), ((), ()), 'just separator')
        self.assertEqual(r._string_to_rule('1/'), ((1,), ()), 'first empty')
        self.assertEqual(r._string_to_rule('/2'), ((), (2,)), 'second empty')
        self.assertEqual(r._string_to_rule('1/2'), ((1,), (2,)), '1 by 1.')
        self.assertEqual(
            r._string_to_rule('  5  6  /  7  8  \r\n\t!"$%^&*()'),
            ((5, 6), (7, 8)),
            'ignore invalid characters')
        self.assertEqual(r._string_to_rule('12/3'), ((1, 2), (3,)), '2 by 1')
        self.assertEqual(
            r._string_to_rule('12/34'), ((1, 2), (3, 4)),
            '2 by 2')
        self.assertEqual(r._string_to_rule('1/2/3'), ((1,), (2,)), '>2')

    def test_rule_parser_from_text_and_back(self):
        rule_text = '45/89'
        rule = r.Rule(rule_text)
        self.assertEqual(str(rule), rule_text)

    @patch('builtins.print')
    def test_main(self, mock_print) -> None:
        r.main()
        mock_print.assert_any_call(
            'Standard Conway rules (Born/Survives): 3/23')
