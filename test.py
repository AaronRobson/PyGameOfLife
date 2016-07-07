#!/usr/bin/python

#Unit testing

import unittest

import GameOfLifeGUI
import GameOfLife
import colourutils
import counter
import cellfile

'''TODO:
Test: GameOfLifeGUI
'''

class TestRuleClass(unittest.TestCase):
  def setUp(self):
    self.support = GameOfLife
    self.widget = self.support.Rule()

  def testString(self):
    self.assertEqual(self.widget.string, '3/23', 'Default rule string incorrect.')

    self.widget.string = '12/23'
    self.assertEqual(self.widget.string, '12/23', '')
    self.assertEqual(str(self.widget), '12/23', '')

    self.assertEqual(self.widget._rule, ((1,2),(2,3)), 'Test internal rule storage as white box.')

    self.widget.string = '9876543210/'
    self.assertEqual(self.widget._rule, ((0,1,2,3,4,5,6,7,8,9), ()), '')

    self.widget.string = '/11'
    self.assertEqual(self.widget._rule, ((), (1,)), '')

    self.widget.string = ''
    self.assertEqual(self.widget._rule, ((), ()), '')

  def testIsAliveNextGeneration(self):
    self.assertTrue(self.widget.IsAliveNextGeneration(True, 3), '')
    self.assertTrue(self.widget.IsAliveNextGeneration(True, 2), '')
    self.assertTrue(self.widget.IsAliveNextGeneration(False, 3), '')

    self.assertFalse(self.widget.IsAliveNextGeneration(True, 4), '')
    self.assertFalse(self.widget.IsAliveNextGeneration(True, 1), '')
    self.assertFalse(self.widget.IsAliveNextGeneration(False, 4), '')
    self.assertFalse(self.widget.IsAliveNextGeneration(False, 2), '')

    self.widget.string = '23/12'

    self.assertTrue(self.widget.IsAliveNextGeneration(True, 1), '')
    self.assertTrue(self.widget.IsAliveNextGeneration(True, 2), '')
    self.assertTrue(self.widget.IsAliveNextGeneration(False, 2), '')
    self.assertTrue(self.widget.IsAliveNextGeneration(False, 3), '')

    self.assertFalse(self.widget.IsAliveNextGeneration(True, 3), '')
    self.assertFalse(self.widget.IsAliveNextGeneration(True, 0), '')
    self.assertFalse(self.widget.IsAliveNextGeneration(False, 4), '')
    self.assertFalse(self.widget.IsAliveNextGeneration(False, 1), '')

  def test_StringToDigitTuple(self):
    self.assertEqual(self.widget._StringToDigitTuple(''), (), '')
    self.assertEqual(self.widget._StringToDigitTuple('jasdjf £€$ ;\!"£$%^//&*()\'#;[]\':{:\')'), (), '')
    self.assertEqual(self.widget._StringToDigitTuple('93648261'), (1,2,3,4,6,8,9), '')
    self.assertEqual(self.widget._StringToDigitTuple('djksd2kdfadfk3kfa;@~}1'), (1,2,3), '')
    self.assertEqual(self.widget._StringToDigitTuple('11111111111111111111adjfa33333333jdfj5555'), (1,3,5), '')

  def test_RuleToString(self):
    self.assertEqual(self.widget._RuleToString(((), ())), '/', 'RuleToString Fail: on empty notation.')
    self.assertEqual(self.widget._RuleToString(((1,), (2,))), '1/2', 'RuleToString Fail: on standard notation 1 by 1.')
    self.assertEqual(self.widget._RuleToString(((1,2,), (3,))), '12/3', 'RuleToString Fail: on standard notation 2 by 1.')
    self.assertEqual(self.widget._RuleToString(((1,2,), (3,4,))), '12/34', 'RuleToString Fail: on standard notation extended 2 by 2.')
    self.assertEqual(self.widget._RuleToString(((1,), (2,), (3,))), '1/2', 'RuleToString Fail: on more than two rule sections.')

  def test_StringToRule(self):
    self.assertEqual(self.widget._StringToRule(), ((3,), (2,3,)), 'StringToRule Fail: default rule incorrect.')
    self.assertEqual(self.widget._StringToRule(''), ((), ()), 'StringToRule Fail: on empty notation.')
    self.assertEqual(self.widget._StringToRule('/'), ((), ()), 'StringToRule Fail: on only separator notation.')
    self.assertEqual(self.widget._StringToRule('1/'), ((1,), ()), 'StringToRule Fail: on first empty.')
    self.assertEqual(self.widget._StringToRule('/2'), ((), (2,)), 'StringToRule Fail: on second empty.')
    self.assertEqual(self.widget._StringToRule('1/2'), ((1,), (2,)), 'StringToRule Fail: on standard notation 1 by 1.')
    self.assertEqual(self.widget._StringToRule('  5  6  /  7  8  \r\n\t!"£$%^&*()'), ((5,6), (7,8)), 'StringToRule Fail: Fails to ignore whitespace and other characters properly.')
    self.assertEqual(self.widget._StringToRule('12/3'), ((1,2,), (3,)), 'StringToRule Fail: on standard notation 2 by 1.')
    self.assertEqual(self.widget._StringToRule('12/34'), ((1,2,), (3,4,)), 'StringToRule Fail: on standard notation extended 2 by 2.')
    self.assertEqual(self.widget._StringToRule('1/2/3'), ((1,), (2,)), 'StringToRule Fail: on more than two rule sections.')

  def test_RuleParserFromString_GetRule_RuleToString(self):
    ruleStr = '45/89'
    self.widget.string = ruleStr
    #self.assertEqual(self.widget.rule, ((4,5), (8,9)), 'RuleParserFromString & GetRule & RuleToString Fail: custom 2 by 2 rule incorrectly stored.')
    self.assertEqual(self.widget.string, ruleStr, 'RuleParserFromString & GetRule & RuleToString Fail: custom 2 by 2 rule round trip change.')

class TestCounterClass(unittest.TestCase):
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

class TestGameOfLifeClass(unittest.TestCase):
  def setUp(self):
    self.support = GameOfLife
    self.widget = self.support.GameOfLifeClass()

  def testProductOfSeq(self):
    self.assertEqual(self.support.ProductOfSeq((1, 2, 3)), 6, 'ProductOfSeq Fail: on simple integer multiplication.')
    self.assertEqual(self.support.ProductOfSeq((1/2, 2/1, 3/5, 5/3)), 1, 'ProductOfSeq Fail: on opposing fractions.')

  def testAround(self):
    result = self.widget.Around((1,1,1))
    self.assertFalse((1,1,1) in result, 'Around Fail: centre cell not being removed from result.')
    self.assertTrue((1,1,2) in result, 'Around Fail: not including normal values around centre cell.')
    self.assertTrue((0,0,0) in result, 'Around Fail: not including low values around centre cell.')
    self.assertTrue((2,2,2) in result, 'Around Fail: not including high values around centre cell.')
    self.assertFalse((3,1,1) in result, 'Around Fail: value out of range included.')

  def testAroundInclusive(self):
    result = self.widget.AroundInclusive((1,1,1))
    self.assertTrue((1,1,1) in result, 'Around Inclusive Fail: centre cell being removed from result.')
    self.assertTrue((1,1,2) in result, 'Around Inclusive Fail: not including normal values around centre cell.')
    self.assertTrue((0,0,0) in result, 'Around Inclusive Fail: not including low values around centre cell.')
    self.assertTrue((2,2,2) in result, 'Around Inclusive Fail: not including high values around centre cell.')
    self.assertFalse((3,1,1) in result, 'Around Inclusive Fail: value out of range included.')

  def testAroundList(self):
    aroundListResult = self.widget.AroundList((3,4), (0,2))
    expectedResult = (0,2), (0,3), (0,4), (0,5), (1,2), (1,3), (1,4), (1,5), (2,2), (2,3), (2,4), (2,5)
    self.assertEqual(aroundListResult, expectedResult, '')

  def testCountAround(self):
    #Glider
    self.widget.SetCells((1,0),(2,1),(0,2),(1,2),(2,2))

    self.assertEqual(self.widget.CountAround((1,1)), 5, '')
    self.assertEqual(self.widget.CountAround((1,3)), 3, '')
    self.assertEqual(self.widget.CountAround((3,3)), 1, '')
    self.assertEqual(self.widget.CountAround((-1,-1)), 0, '')

  def testAffectableCells(self):
    x = 1
    y = 5
    self.widget.SetCell((x,y))
    expected = (x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1),(x,y), (x,y+1), (x+1,y-1), (x+1,y), (x+1,y+1)
    self.assertEqual(self.widget.AffectableCells(), expected, 'AffectableCells incorrect.')

  def testSetCells_Iterate__call__(self):
    exampleKeyList = (0,1), (1,1), (2,1)
    self.assertEqual(self.widget(), (), 'SetCells & __call__ Fail: point listing type or contents incorrect at start.')
    self.widget.SetCells(*exampleKeyList)
    self.assertEqual(self.widget(), exampleKeyList, 'SetCells & __call__ Fail: point listing type or contents incorrect after points added.')

    self.widget.Iterate()
    self.assertEqual(self.widget(), ((1,0), (1,1), (1,2)), 'SetCells & Iterate & __call__ Fail: point listing type or contents incorrect after blinker has one iteration.')

  def testFixRange(self):
    self.assertEqual(self.widget.FixRange((-1,-1), (0,0)), ((1,1), (-1,-1)), 'FixRange Fail: incorrectly handles minus size.')

  def testRandomBoolean(self):
    possiblities = True, False
    for i in range(10):
      self.assertTrue(self.support.RandomBoolean() in possiblities, '')

class TestColourUtils(unittest.TestCase):
  def setUp(self):
    self.support = colourutils

  def testHexPlain(self):
    self.assertEqual(self.support.HexPlain(0xF0), 'F0', '')
    self.assertEqual(self.support.HexPlain(0xF0F0F0), 'F0F0F0', '')

  def testHexPlainPadded(self):
    self.assertEqual(self.support.HexPlainPadded(0xF0, 6), '0000F0', '')
    self.assertEqual(self.support.HexPlainPadded(0xF0F0F0, 6), 'F0F0F0', '')

  def testHexColourPadded(self):
    self.assertEqual(self.support.HexColourPadded(0xF0), '0000F0', '')
    self.assertEqual(self.support.HexColourPadded(0xF0F0F0), 'F0F0F0', '')

  def testStandardHexColourPadded(self):
    self.assertEqual(self.support.StandardHexColourPadded(0xF0), '0x0000F0', '')
    self.assertEqual(self.support.StandardHexColourPadded(0xF0F0F0), '0xF0F0F0', '')

  def testTKHexColourPadded(self):
    self.assertEqual(self.support.TKHexColourPadded(0xF0), '#0000F0', '')
    self.assertEqual(self.support.TKHexColourPadded(0xF0F0F0), '#F0F0F0', '')

  def testColourNumberIsValid(self):
    self.assertFalse(self.support.ColourNumberIsValid(0x1000000), 'Outside lower limit.')
    self.assertTrue(self.support.ColourNumberIsValid(0xFFFFFF), 'Within lower limit')
    self.assertTrue(self.support.ColourNumberIsValid(0x101010), 'Nominal.')
    self.assertTrue(self.support.ColourNumberIsValid(0), 'Within upper limit.')
    self.assertFalse(self.support.ColourNumberIsValid(-1), 'Outside upper limit.')

def RunTests(*testClasses):
  """if no specific test classes are wanted add all of them."""
  #http://docs.python.org/library/unittest.html
  #http://diveintopython.org/unit_testing/index.html
  #http://diveintopython.org/unit_testing/testing_for_success.html
  #http://diveintopython.org/unit_testing/testing_for_failure.html
  #To check for exceptions being called; search for assertRaises in: http://diveintopython.org/unit_testing/testing_for_sanity.html

  print('--Testing Start--')

  if len(testClasses) == 0:
    testClasses = testClassesToRun

  for tc in testClasses:
    print('\n\n%s:\n' % tc.__name__)
    suite = unittest.TestLoader().loadTestsFromTestCase(tc)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

  print('\n\n--Testing End--\n')

'''Important that this links to all Test Classes (those sub-classed from unittest.TestCase) otherwise they will not be run
to run just one, ensure there is a comma afterwards (otherwise with just brackets it is assumed to be a single object and not a collection)'''
testClassesToRun = (TestColourUtils, TestCounterClass, TestRuleClass, TestGameOfLifeClass,)

if __name__ == "__main__":
  print('Unit testing')
  RunTests()
