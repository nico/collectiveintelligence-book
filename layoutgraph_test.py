import unittest
import layoutgraph

class TestinterceptTest(unittest.TestCase):

  def testIntersect(self):
    l1 = ( (400, 10), (30, 50) )
    l2 = ( (40, 40), (400, 400) )
    self.assertTrue(layoutgraph.testintersect(l1, l2))

    l1 = ( (340,  10), (65, 370) )
    l2 = ( (190, 290), (100, 290) )
    self.assertTrue(layoutgraph.testintersect(l1, l2))

  def testNoIntersect(self):
    l1 = ( (400, 10), (30, 50) )
    l2 = ( (500, 40), (600, 400) )
    self.assertFalse(layoutgraph.testintersect(l1, l2))

  def testEndpointTouches(self):
    l1 = ( (0, 0), (10, 10) )
    l2 = ( (20, 0), (10, 10) )
    self.assertFalse(layoutgraph.testintersect(l1, l2))

  #def testParallelTouch(self):  # currently fails
    #l1 = ( (0, 0), (10, 10) )
    #l2 = ( (0, 0), (10, 10) )
    #self.assertTrue(layoutgraph.testintersect(l1, l2))

    #l1 = ( (0, 0), (10, 10) )
    #l2 = ( (4, 4), (6, 6) )
    #self.assertTrue(layoutgraph.testintersect(l1, l2))

    #l1 = ( (0, 0), (10, 10) )
    #l2 = ( (5, 5), (15, 15) )
    #self.assertTrue(layoutgraph.testintersect(l1, l2))

    #l1 = ( (0, 0), (10, 10) )
    #l2 = ( (-5, -5), (5, 5) )
    #self.assertTrue(layoutgraph.testintersect(l1, l2))

  def testParallelNoTouch(self):
    l1 = ( (0, 0), (10, 10) )
    l2 = ( (0, 10), (10, 30) )
    self.assertFalse(layoutgraph.testintersect(l1, l2))

  def testEndpointTouchesParallel(self):
    l1 = ( (0, 0), (10, 10) )
    l2 = ( (20, 20), (10, 10) )
    self.assertFalse(layoutgraph.testintersect(l1, l2))


class VecAngleTest(unittest.TestCase):

  def testAngle(self):
    a = layoutgraph.vec_angle( (10, 5), (5, 5), (5, 10) )
    self.assertAlmostEquals(90.0, a)


if __name__ == '__main__':
  unittest.main()

