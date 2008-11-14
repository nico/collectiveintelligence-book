import unittest

import generatefeedvector


class GetwordsTest(unittest.TestCase):

  def testBasics(self):
    d = '<hallo>this</hallo> is text'
    expected = ['this', 'is', 'text']
    self.assertEquals(expected, generatefeedvector.getwords(d))
       

if __name__ == '__main__':
  unittest.main()

