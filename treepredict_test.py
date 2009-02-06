import unittest

import treepredict


class TestdataTest(unittest.TestCase):

  def testLoads(self):
    self.assertEquals(treepredict.testdata(),
        [['slashdot','USA','yes',18,'None'],
         ['google','France','yes',23,'Premium'],
         ['digg','USA','yes',24,'Basic'],
         ['kiwitobes','France','yes',23,'Basic'],
         ['google','UK','no',21,'Premium'],
         ['(direct)','New Zealand','no',12,'None'],
         ['(direct)','UK','no',21,'Basic'],
         ['google','USA','no',24,'Premium'],
         ['slashdot','France','yes',19,'None'],
         ['digg','USA','no',18,'None'],
         ['google','UK','no',18,'None'],
         ['kiwitobes','UK','no',19,'None'],
         ['digg','New Zealand','yes',12,'Basic'],
         ['slashdot','UK','no',21,'None'],
         ['google','UK','yes',18,'Basic'],
         ['kiwitobes','France','yes',19,'Basic']])


class DividesetTest(unittest.TestCase):

  def testIntegerDivide(self):
    self.assertEquals(([(3,), (4,)], [(1,), (2,)]),
        treepredict.divideset([(1,), (2,), (3,), (4,)], 0, 3))

  def testFloatDivide(self):
    self.assertEquals(([(3.0,), (4.0,)], [(1.0,), (2.0,)]),
        treepredict.divideset([(1.0,), (2.0,), (3.0,), (4.0,)], 0, 3.0))

  def testStringDivide(self):
    self.assertEquals(([('a',)], [('b',), ('c',)]),
        treepredict.divideset([('a',), ('b',), ('c',)], 0, 'a'))


class GiniimpurityTest(unittest.TestCase):

  def testBasics(self):
    d = treepredict.testdata()
    self.assertAlmostEquals(0.6328125, treepredict.giniimpurity(d))

    s1, s2 = treepredict.divideset(d, 2, 'yes')
    self.assertAlmostEquals(0.53125, treepredict.giniimpurity(s1))


class EntropyTest(unittest.TestCase):

  def testBasics(self):
    d = treepredict.testdata()
    self.assertAlmostEquals(1.5052408, treepredict.entropy(d))

    s1, s2 = treepredict.divideset(d, 2, 'yes')
    self.assertAlmostEquals(1.2987949, treepredict.entropy(s1))


class ClassifyTest(unittest.TestCase):

  def testBasics(self):
    t = treepredict.buildtree(treepredict.testdata())
    self.assertEquals(treepredict.classify(['(direct)', 'USA', 'yes', 5], t),
        {'Basic': 4})


if __name__ == '__main__':
  unittest.main()
