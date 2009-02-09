import unittest

import numpredict

class PartitionTest(unittest.TestCase):

  def testBasic(self):
    self.assertEquals( ([1, 3, 5], [2, 4]),
        numpredict.partition(range(1, 6), lambda itm: itm % 2 != 0))


if __name__ == '__main__':
  unittest.main()
