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


class BiclusterTest(unittest.TestCase):

  def testEquals(self):
    a = clusters.bicluster([1, 2, 3])
    b = clusters.bicluster([1, 2, 3])
    self.assertEquals(a, b)
    self.assertFalse(a != b)

    self.assertEquals(clusters.bicluster([], left=a),
                      clusters.bicluster([], left=b))
    self.assertEquals(clusters.bicluster([], right=a),
                      clusters.bicluster([], right=b))
    self.assertEquals(clusters.bicluster([], distance=2.5),
                      clusters.bicluster([], distance=2.5))
    self.assertEquals(clusters.bicluster([], id=5),
                      clusters.bicluster([], id=5))


class HclusterTest(unittest.TestCase):

  def testNormal(self):
    rows = [[6, 4, 2],
            [2, 4, 6],
            [1, 2, 3],
            [3, 2, 1.01]]


    clust = [clusters.bicluster(rows[i], id=i) for i in range(len(rows))]

    c0 = clusters.bicluster(clusters.mergevecs(rows[1], rows[2]),
      left=clust[1], right=clust[2], id=-1, distance=0.0)
    c1 = clusters.bicluster(clusters.mergevecs(rows[0], rows[3]),
      left=clust[0], right=clust[3], id=-2,
      distance=clusters.pearson_dist(rows[0], rows[3]))
    c2 = clusters.bicluster(clusters.mergevecs(c0.vec, c1.vec),
      left=c0, right=c1, id=-3,
      distance=clusters.pearson_dist(c0.vec, c1.vec))

    self.assertEquals(c2, clusters.hcluster(rows))


class TransposeTest(unittest.TestCase):

  def test1x3(self):
    self.assertEquals([[1], [2], [3]], clusters.transpose([[1, 2, 3]]))

  def test3x1(self):
    self.assertEquals([[1, 2, 3]], clusters.transpose([[1], [2], [3]]))

  def test2x2(self):
    self.assertEquals([[1, 2], [5, 3]], clusters.transpose([[1, 5], [2, 3]]))


class RowbbTest(unittest.TestCase):

  def testNormal(self):
    m = [[-1,  4],
         [ 0,  0],
         [ 8, -5]]
    self.assertEquals([(-1, 8), (-5, 4)], clusters.rowbb(m))


class GetnearestTest(unittest.TestCase):

  def testNormal(self):

    points = [[1, 2, 3], [-2, -4, -6], [1, 0, 1]]
    self.assertEquals(0, clusters.getnearest([2, 4, 6], points,
      clusters.pearson_dist))
    self.assertEquals(1, clusters.getnearest([-1, -2, -3], points,
      clusters.pearson_dist))
    self.assertEquals(2, clusters.getnearest([2, 0, 2], points,
      clusters.pearson_dist))


class AverageTest(unittest.TestCase):

  def testNormal(self):

    m = [[-1,  4],
         [ 0,  0],
         [ 8, -5]]

    self.assertEquals([7.0/2, -1.0/2], clusters.average([0, 2], m))


class KclusterTest(unittest.TestCase):

  def testNormal(self):
    m = [[ 1,  2],
         [ 0, -1],
         [ 2,  4]]

    self.assertEquals([[0, 2], [1]], sorted(clusters.kcluster(m, k=2)))


class EuclDistTest(unittest.TestCase):

  def testNormal(self):

    self.assertAlmostEquals(5, clusters.hypot([3, 4]))
    self.assertAlmostEquals(5, clusters.hypot([3, 3, 1, 1, 1, 1, 1, 1, 1]))
    self.assertAlmostEquals(5, clusters.euclid_dist([0, 0, 0], [3, 4, 0]))


class ScaledownTest(unittest.TestCase):

  def testNormal(self):

    m = [[1, 0, 2, 0],
         [2, 0, 3, 0]]

    r = clusters.scaledown(m, distance=clusters.euclid_dist, rate=0.1)
    self.assertEquals(2, len(r))
    self.assertAlmostEquals(clusters.euclid_dist(m[0], m[1]),
        clusters.euclid_dist(r[0], r[1]))


if __name__ == '__main__':
  unittest.main()
