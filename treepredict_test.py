import unittest

import treepredict

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

if __name__ == '__main__':
  unittest.main()
