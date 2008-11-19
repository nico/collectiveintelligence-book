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
    rows = [[0, 0, 0],
            [2, 4, 6],
            [1, 2, 3]]


    clust = [clusters.bicluster(rows[i], id=i) for i in range(len(rows))]

    c0 = clusters.bicluster(clusters.mergevecs(rows[1], rows[2]),
      left=clust[1], right=clust[2], id=-1, distance=0.0)
    c1 = clusters.bicluster(clusters.mergevecs(rows[0], c0.vec),
      left=clust[0], right=c0, id=-2,
      distance=clusters.pearson_dist(rows[0], c0.vec))

    self.assertEquals(c1, clusters.hcluster(rows))


if __name__ == '__main__':
  unittest.main()
