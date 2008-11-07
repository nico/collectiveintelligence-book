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


class TopMatchesTest(unittest.TestCase):
  def setUp(self):
    self.data = {
        'Nico': { 'Python': 4.5, 'Ruby': 3.0, 'C++': 3.4, 'Java': 2.5 },
        'Yann': { 'Python': 3.0, 'Ruby': 4.5, 'C++': 3.4, 'Java': 1.5 },
        'Josh': { 'Python': 0.5, 'Ruby': 0.0, 'C++': 1.0, 'Java': 5.0 },
        'Kerstin': { 'Chocolate': 5.0 },
        }

  def testBasics(self):
    scores = { 'Yann': 3, 'Kerstin': 2, 'Josh': 1 }
    def stubDistance(prefs, p1, p2):
      self.assertEquals(self.data, prefs)
      if p1 == 'Nico': return scores[p2]
      else: return scores[p1]
    m = recommendations.topMatches(self.data, 'Nico', similarity=stubDistance)
    self.assertEquals([(3, 'Yann'), (2, 'Kerstin'), (1, 'Josh')], m)

  def testNormalWithPearson(self):
    m = recommendations.topMatches(self.data, 'Nico',
        similarity=recommendations.sim_pearson)
    # With pearson, disagreement is worse than no common ground
    self.assertEquals(['Yann', 'Kerstin', 'Josh'], [n for (s,n) in m])

  def testNormalWithDistance(self):
    m = recommendations.topMatches(self.data, 'Nico',
        similarity=recommendations.sim_distance)
    # With distance, disagreement is closer than no common ground
    self.assertEquals(['Yann', 'Josh', 'Kerstin'], [n for (s,n) in m])

  def testNLargetThanCount(self):
    m = recommendations.topMatches(self.data, 'Kerstin', n=2*len(self.data))
    self.assertEquals(len(self.data) - 1, len(m))

class GetRecommendationsTest(unittest.TestCase):
  def setUp(self):
    self.data = {
        'Nico': { 'Python': 4.5, 'Ruby': 3.0, 'C++': 3.4, 'Java': 2.5 },
        'Yann': { 'Python': 3.0, 'Ruby': 4.5, 'C++': 3.4, 'Java': 1.5,
                  'Mathematica': 3.5, 'Chocolate': 2.0, 'Patterns': 2.0 },
        'Josh': { 'Python': 0.5, 'Ruby': 0.0, 'C++': 1.0, 'Java': 5.0,
                  'Patterns': 5.0 },
        'Kerstin': { 'Python': 0.1, 'Chocolate': 5.0 },
        }

  def testBasics(self):
    r = recommendations.getRecommendations(self.data, 'Nico',
        similarity=recommendations.sim_distance)
    #print recommendations.sim_distance(self.data, 'Nico', 'Yann')
    #print recommendations.sim_distance(self.data, 'Nico', 'Josh')
    #print recommendations.sim_distance(self.data, 'Nico', 'Kerstin')
    #print r
    self.assertEquals(['Mathematica', 'Chocolate', 'Patterns'],
        [n for s,n in r])

class TransformPrefsTest(unittest.TestCase):
  def testBasics(self):
    d = { 'a': {'b': 0.4}, 'c': {'d': 0.5} }
    expected = { 'b': {'a': 0.4}, 'd': {'c' : 0.5} }
    self.assertEquals(expected, recommendations.transformPrefs(d))

  def testEmptyPrefsList(self):
    d = { 'a': {}, 'c': {'d': 0.5} }
    expected = { 'd': {'c' : 0.5} }
    self.assertEquals(expected, recommendations.transformPrefs(d))

  def testOnlyEmptyPrefs(self):
    d = { 'a': {} }
    expected = { }
    self.assertEquals(expected, recommendations.transformPrefs(d))

  def testAllEmpty(self):
    d = { }
    expected = { }
    self.assertEquals(expected, recommendations.transformPrefs(d))

  def testCollect(self):
    d = { 'a': {'z': 0.1}, 'b': {'z' : 0.2}, 'c': {'z': 0.3} }
    expected = { 'z': {'a': 0.1, 'b': 0.2, 'c': 0.3} }
    self.assertEquals(expected, recommendations.transformPrefs(d))


class GetRecommendedItemsTest(unittest.TestCase):
  def testBasics(self):
    d = {'N': {'p': 1.0, 'j': 0.3}, 'Y':{'p': 0.8, 'j': 0.2, 'r':1.0} }
    itemsim = recommendations.calculateSimilarItems(d)
    r = recommendations.getRecommendedItems(d, itemsim, 'N')
    self.assertEquals(1, len(r))
    self.assertEquals('r', r[0][1])
       

class SimTanimotoTestCase(DistanceTestCase, unittest.TestCase):
  def setUp(self):
    self.metric = recommendations.sim_tanimoto
    self.prefs = { 'Nico': {'h': 0.8, 'b':0.2}, 'Yann': {'h': 0.4, 'b':0.1}}

  def testNormal(self):
    expected = (0.32 + 0.02) / ((0.64 + 0.04) + (0.16 + 0.01) - (0.32 + 0.02))
    self.assertAlmostEquals(expected, self.metric(self.prefs, 'Nico', 'Yann'))


if __name__ == '__main__':
  unittest.main()
