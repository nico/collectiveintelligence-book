import unittest

import recommendations

class SimDistanceTestCase(unittest.TestCase):

  def testNormal(self):
    prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1}}
    self.assertAlmostEquals(0.7080596,
        recommendations.sim_distance(prefs, 'Nico', 'Yann'))

  def testAdditionalLeft(self):
    prefs = { 'Nico': {'h': 0.8, 'b':0.2, 'c':0.9}, 'Yann': {'h': 0.4, 'b':0.1}}
    self.assertAlmostEquals(0.7080596,
        recommendations.sim_distance(prefs, 'Nico', 'Yann'))

  def testAdditionalRight(self):
    prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1, 'c':0.9}}
    self.assertAlmostEquals(0.7080596,
        recommendations.sim_distance(prefs, 'Nico', 'Yann'))

  def testIdentical(self):
    prefs = { 'Nico': {'h': 1}, 'Yann': {'h': 1}}
    self.assertEquals(1.0, recommendations.sim_distance(prefs, 'Nico', 'Yann'))

  def testEmptyPrefs(self):
    prefs = { 'Nico': {}, 'Yann': {}}
    self.assertEquals(0.0, recommendations.sim_distance(prefs, 'Nico', 'Yann'))

  def testEmptyIntersection(self):
    prefs = { 'Nico': {'h': 1}, 'Yann': {'z': 1}}
    self.assertEquals(0.0, recommendations.sim_distance(prefs, 'Nico', 'Yann'))


if __name__ == '__main__':
  unittest.main()
