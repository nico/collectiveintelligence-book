import unittest

import clusters

class DoReadfileTest(unittest.TestCase):

  def testNormal(self):
    lines = ['x\ta\tb\tc',
             'd\t0\t1\t2',
             'e\t3\t4\t5',
            ]

    rownames, colnames, data = clusters.do_readfile(lines)
    self.assertEquals(['d', 'e'], rownames)
    self.assertEquals(['a', 'b', 'c'], colnames)
    self.assertEquals([[0, 1, 2], [3, 4, 5]], data)

if __name__ == '__main__':
  unittest.main()
