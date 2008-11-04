import unittest

import recommendations

class DistanceTestCase:

  def testIdentical(self):
    prefs = { 'Nico': {'h': 1, 'b':0.4}, 'Yann': {'h': 1, 'b': 0.4}}
    self.assertEquals(1.0, self.metric(prefs, 'Nico', 'Yann'))

  def testOneEqualElement(self):
    prefs = { 'Nico': {'h': 0.9}, 'Yann': {'h': 0.9}}
    self.assertEquals(1.0, self.metric(prefs, 'Nico', 'Yann'))

  def testEmptyPrefs(self):
    prefs = { 'Nico': {}, 'Yann': {}}
    self.assertEquals(0.0, self.metric(prefs, 'Nico', 'Yann'))

  def testEmptyIntersection(self):
    prefs = { 'Nico': {'h': 1}, 'Yann': {'z': 1}}
    self.assertEquals(0.0, self.metric(prefs, 'Nico', 'Yann'))

  def testAdditionalLeft(self):
    addLeft = self.prefs.copy()
    addLeft['Nico']['c'] = 0.9
    self.assertAlmostEquals(self.metric(self.prefs, 'Nico', 'Yann'),
        self.metric(addLeft, 'Nico', 'Yann'))

  def testAdditionalRight(self):
    addRight = self.prefs.copy()
    addRight['Yann']['c'] = 0.9
    self.assertAlmostEquals(self.metric(self.prefs, 'Nico', 'Yann'),
        self.metric(addRight, 'Nico', 'Yann'))


class SimDistanceTestCase(DistanceTestCase, unittest.TestCase):
  def setUp(self):
    self.metric = recommendations.sim_distance
    self.prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1}}

  def testNormal(self):
    self.assertAlmostEquals(0.7080596, self.metric(self.prefs, 'Nico', 'Yann'))


class SimPearsonTestCase(DistanceTestCase, unittest.TestCase):
  def setUp(self):
    self.metric = recommendations.sim_pearson
    self.prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1}}

  def testNormal(self):
    self.assertAlmostEquals(1, self.metric(self.prefs, 'Nico', 'Yann'))



if __name__ == '__main__':
  unittest.main()
