#!/usr/bin/python

import unittest

import GameOfLifeGUI
import GameOfLife
import colourutils
import counter
import cellfile
import rule

'''TODO:
Test: GameOfLifeGUI
'''

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
    self.assertEqual(rule.survives, (2,3), '')

    rule = self.widget('12/23')
    self.assertEqual(rule.born, (1,2), '')
    self.assertEqual(rule.survives, (2,3), '')

    rule = self.widget('23/12')
    self.assertEqual(rule.born, (2,3), '')
    self.assertEqual(rule.survives, (1,2), '')

    rule = self.widget('9876543210/')
    self.assertEqual(rule.born, (0,1,2,3,4,5,6,7,8,9), '')
    self.assertEqual(rule.survives, (), '')

    rule = self.widget('/11')
    self.assertEqual(rule.born, (), '')
    self.assertEqual(rule.survives, (1,), '')

    rule = self.widget('')
    self.assertEqual(rule.born, (), '')
    self.assertEqual(rule.survives, (), '')

  def test_StringToDigitTuple(self):
    self.assertEqual(self.support._StringToDigitTuple(''), (), '')
    self.assertEqual(self.support._StringToDigitTuple('jasdjf £$ ;\!"£$%^//&*()\'#;[]\':{:\')'), (), '')
    self.assertEqual(self.support._StringToDigitTuple('93648261'), (1,2,3,4,6,8,9), '')
    self.assertEqual(self.support._StringToDigitTuple('djksd2kdfadfk3kfa;@~}1'), (1,2,3), '')
    self.assertEqual(self.support._StringToDigitTuple('11111111111111111111adjfa33333333jdfj5555'), (1,3,5), '')

  def test_RuleToString(self):
    self.assertEqual(self.support._RuleToString(((), ())), '/', 'RuleToString Fail: on empty notation.')
    self.assertEqual(self.support._RuleToString(((1,), (2,))), '1/2', 'RuleToString Fail: on standard notation 1 by 1.')
    self.assertEqual(self.support._RuleToString(((1,2,), (3,))), '12/3', 'RuleToString Fail: on standard notation 2 by 1.')
    self.assertEqual(self.support._RuleToString(((1,2,), (3,4,))), '12/34', 'RuleToString Fail: on standard notation extended 2 by 2.')
    self.assertEqual(self.support._RuleToString(((1,), (2,), (3,))), '1/2', 'RuleToString Fail: on more than two rule sections.')

  def test_StringToRule(self):
    self.assertEqual(self.support._StringToRule(), ((3,), (2,3,)), 'StringToRule Fail: default rule incorrect.')
    self.assertEqual(self.support._StringToRule(''), ((), ()), 'StringToRule Fail: on empty notation.')
    self.assertEqual(self.support._StringToRule('/'), ((), ()), 'StringToRule Fail: on only separator notation.')
    self.assertEqual(self.support._StringToRule('1/'), ((1,), ()), 'StringToRule Fail: on first empty.')
    self.assertEqual(self.support._StringToRule('/2'), ((), (2,)), 'StringToRule Fail: on second empty.')
    self.assertEqual(self.support._StringToRule('1/2'), ((1,), (2,)), 'StringToRule Fail: on standard notation 1 by 1.')
    self.assertEqual(self.support._StringToRule('  5  6  /  7  8  \r\n\t!"£$%^&*()'), ((5,6), (7,8)), 'StringToRule Fail: Fails to ignore whitespace and other characters properly.')
    self.assertEqual(self.support._StringToRule('12/3'), ((1,2,), (3,)), 'StringToRule Fail: on standard notation 2 by 1.')
    self.assertEqual(self.support._StringToRule('12/34'), ((1,2,), (3,4,)), 'StringToRule Fail: on standard notation extended 2 by 2.')
    self.assertEqual(self.support._StringToRule('1/2/3'), ((1,), (2,)), 'StringToRule Fail: on more than two rule sections.')

  def test_RuleParserFromString_GetRule_RuleToString(self):
    ruleStr = '45/89'
    rule = self.widget(ruleStr)
    self.assertEqual(str(rule), ruleStr, 'RuleParserFromString & GetRule & RuleToString Fail: custom 2 by 2 rule round trip change.')

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

class TestGameOfLife(unittest.TestCase):
  def setUp(self):
    self.support = GameOfLife
    self.widget = self.support.GameOfLife()

  def test_Around(self):
    result = list(self.support.Around((1,1,1)))
    self.assertFalse((1,1,1) in result, 'Around Fail: centre cell not being removed from result.')
    self.assertTrue((1,1,2) in result, 'Around Fail: not including normal values around centre cell.')
    self.assertTrue((0,0,0) in result, 'Around Fail: not including low values around centre cell.')
    self.assertTrue((2,2,2) in result, 'Around Fail: not including high values around centre cell.')
    self.assertFalse((3,1,1) in result, 'Around Fail: value out of range included.')

  def test_MooreNeighborhood(self):
    result = list(self.support.MooreNeighborhood((1,1,1)))
    self.assertTrue((1,1,1) in result, 'MooreNeighborhood Fail: centre cell being removed from result.')
    self.assertTrue((1,1,2) in result, 'MooreNeighborhood Fail: not including normal values around centre cell.')
    self.assertTrue((0,0,0) in result, 'MooreNeighborhood Fail: not including low values around centre cell.')
    self.assertTrue((2,2,2) in result, 'MooreNeighborhood Fail: not including high values around centre cell.')
    self.assertFalse((3,1,1) in result, 'MooreNeighborhood Fail: value out of range included.')

  def test_AroundList(self):
    aroundListResult = list(self.support.AroundList((3,4), (0,2)))
    expectedResult = [(0,2), (0,3), (0,4), (0,5), (1,2), (1,3), (1,4), (1,5), (2,2), (2,3), (2,4), (2,5)]
    self.assertEqual(aroundListResult, expectedResult, '')

  def test_CountAround(self):
    #Glider
    cells = [(1,0),(2,1),(0,2),(1,2),(2,2)]

    self.assertEqual(self.support.CountAround((1,1), cells), 5, '')
    self.assertEqual(self.support.CountAround((1,3), cells), 3, '')
    self.assertEqual(self.support.CountAround((3,3), cells), 1, '')
    self.assertEqual(self.support.CountAround((-1,-1), cells), 0, '')

  def test_AffectableCells(self):
    x = 1
    y = 5
    cells = [(x,y)]
    expected = {(x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1),(x,y), (x,y+1), (x+1,y-1), (x+1,y), (x+1,y+1)}
    self.assertEqual(self.support.AffectableCells(cells), expected, 'AffectableCells incorrect.')

  def test_SetCells_Iterate__call__(self):
    exampleKeyList = {(0,1), (1,1), (2,1)}
    self.assertEqual(self.widget(), set(), 'SetCells & __call__ Fail: point listing type or contents incorrect at start.')
    self.widget.cells = exampleKeyList
    self.assertEqual(self.widget(), exampleKeyList, 'SetCells & __call__ Fail: point listing type or contents incorrect after points added.')

    self.widget.Iterate()
    self.assertEqual(self.widget(), {(1,0), (1,1), (1,2)}, 'SetCells & Iterate & __call__ Fail: point listing type or contents incorrect after blinker has one iteration.')

  def test_FixRange(self):
    self.assertEqual(self.support.FixRange((-1,-1), (0,0)), ((1,1), (-1,-1)), 'FixRange Fail: incorrectly handles minus size.')

  def test_RandomBoolean(self):
    possiblities = True, False
    for i in range(10):
      self.assertTrue(self.support.RandomBoolean() in possiblities, '')

  def test_population(self):
    self.assertEqual(self.widget.population, 0)
    self.assertEqual(len(self.widget), 0)

    #Glider
    self.widget.cells = [(1,0),(2,1),(0,2),(1,2),(2,2)]

    self.assertEqual(self.widget.population, 5)
    self.assertEqual(len(self.widget), 5)

class TestColourUtils(unittest.TestCase):
  def setUp(self):
    self.support = colourutils

  def test_HexPlain(self):
    self.assertEqual(self.support.HexPlain(0xF0), 'F0', '')
    self.assertEqual(self.support.HexPlain(0xF0F0F0), 'F0F0F0', '')

  def test_HexPlainPadded(self):
    self.assertEqual(self.support.HexPlainPadded(0xF0, 6), '0000F0', '')
    self.assertEqual(self.support.HexPlainPadded(0xF0F0F0, 6), 'F0F0F0', '')

  def test_HexColourPadded(self):
    self.assertEqual(self.support.HexColourPadded(0xF0), '0000F0', '')
    self.assertEqual(self.support.HexColourPadded(0xF0F0F0), 'F0F0F0', '')

  def test_StandardHexColourPadded(self):
    self.assertEqual(self.support.StandardHexColourPadded(0xF0), '0x0000F0', '')
    self.assertEqual(self.support.StandardHexColourPadded(0xF0F0F0), '0xF0F0F0', '')

  def test_TKHexColourPadded(self):
    self.assertEqual(self.support.TKHexColourPadded(0xF0), '#0000F0', '')
    self.assertEqual(self.support.TKHexColourPadded(0xF0F0F0), '#F0F0F0', '')

  def test_ColourNumberIsValid(self):
    self.assertFalse(self.support.ColourNumberIsValid(0x1000000), 'Outside lower limit.')
    self.assertTrue(self.support.ColourNumberIsValid(0xFFFFFF), 'Within lower limit')
    self.assertTrue(self.support.ColourNumberIsValid(0x101010), 'Nominal.')
    self.assertTrue(self.support.ColourNumberIsValid(0), 'Within upper limit.')
    self.assertFalse(self.support.ColourNumberIsValid(-1), 'Outside upper limit.')

class TestGameOfLifeGUI(unittest.TestCase):
  def setUp(self):
    self.support = GameOfLifeGUI

  def test_GoingToString(self):
     self.assertEqual(self.support.GoingToString(False), 'Go')
     self.assertEqual(self.support.GoingToString(True), 'Stop')

  def test_BoolToPlusMinusOne(self):
    self.assertEqual(self.support.BoolToPlusMinusOne(False), -1)
    self.assertEqual(self.support.BoolToPlusMinusOne(True), 1)

if __name__ == "__main__":
  unittest.main()
