import unittest
import layoutgraph

class MakecostTest(unittest.TestCase):

  def test1(self):
    f = layoutgraph.makecost(layoutgraph.People, layoutgraph.Links)
    self.assertEquals(3, f([141, 10,  171, 143,  67, 296,  187, 164,
      370, 21,  331, 39,  124, 166,  354, 307]))

if __name__ == '__main__':
  unittest.main()

