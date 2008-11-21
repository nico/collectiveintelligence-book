from math import sqrt
import random


def readfile(filename):
  return do_readfile(open(filename).readlines())


def do_readfile(lines):
  colnames = lines[0].strip().split('\t')[1:]
  rownames = []
  data = []
  for line in lines[1:]:
    p = line.strip().split('\t')
    rownames.append(p[0])
    data.append([float(x) for x in p[1:]])
  return rownames, colnames, data


def pearson(v1, v2):
  """Returns the similarity between v1 and v2.

  1.0 means very similar and 0.0 means no correlation. -1.0 means
  anticorrelation.  v1 and v2 must have the same number of elements."""

  assert len(v1) == len(v2)

  n = len(v1)
  if n == 0: return 0

  sum1 = sum(v1)
  sum2 = sum(v2)

  sqSum1 = sum([pow(v, 2) for v in v1])
  sqSum2 = sum([pow(v, 2) for v in v2])

  pSum = sum([v1[i] * v2[i] for i in range(n)])

  num = pSum - (sum1*sum2/n)
  den = sqrt((sqSum1 - pow(sum1, 2)/n) * (sqSum2 - pow(sum2, 2)/n))
  if den == 0:
    # It's not clear what to do here. It can happen when all components are
    # equal (which means "very similar"), or if one of the vectors contains
    # only zeroes, or if the two vectors contain only one element. In these
    # cases, this function can't figure out how to "scale" its result. Cop
    # out and simply return 0 for those cases.
    return 0

  return num/den


def pearson_dist(v1, v2):
  """0.0 means "near", 1.0 means "far"."""
  return 1 - pearson(v1, v2)


class bicluster(object):
  def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
    self.vec = vec
    self.left = left
    self.right = right
    self.distance = distance
    self.id = id

  def __eq__(self, b):
    return (self.vec == b.vec
        and self.left == b.left
        and self.right == b.right
        and self.distance == b.distance
        and self.id == b.id)

  # If we have __eq__, we better have __ne__ too
  # so that `not (a == b) == a != b`
  def __ne__(self, b):
    return not (self == b)

  # If we have __eq__, we better have __hash__ too
  # so that `a == b => hash(a) == has(b)`. Since we don't need bicluster objects
  # as dict keys, it's ok if this function fails loudly (instead of silently
  # returning a wrong value, which is the defaul)
  def __hash__(self):
    raise NotImplementedError

  def __str__(self):
    return '%s %f %d (%s %s)' % (str(self.vec), self.distance, self.id,
        self.left, self.right)


def mergevecs(a, b):
  return [(a[i] + b[i])/2.0 for i in range(len(a))]


def hcluster(rows, distance=pearson_dist):
  distances = {}
  currentclustid = -1

  # Clusters start off as just rows
  clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

  # O(n^3), yuck! Effectively, only the distance() calls are expensive,
  # and we cache them, this is really O(n^2)
  while len(clust) > 1:
    lowestpair = 0, 1
    closest = distance(clust[0].vec, clust[1].vec)

    # Loop through every pair looking for the smallest distance
    for i in range(len(clust)):
      for j in range(i + 1, len(clust)):
        # cache distances. Makes this much faster.
        # (can't use the cache() function because we cache on indices, not
        # function arguments)
        if (i, j) not in distances:
          distances[i, j] = distance(clust[i].vec, clust[j].vec)
        d = distances[i, j]

        if d < closest:
          closest = d
          lowestpair = i, j

    # Merge closest pair into a single vector
    mergevec = mergevecs(clust[lowestpair[0]].vec, clust[lowestpair[1]].vec)

    newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
        right=clust[lowestpair[1]], distance=closest, id=currentclustid)

    # Update
    currentclustid -= 1
    del clust[lowestpair[1]]  # Need to del() bigger index first!
    del clust[lowestpair[0]]
    clust.append(newcluster)

  return clust[0]


def printclust(clust, labels=None, n=0):
  print ' ' * n,
  if clust.id < 0:  # branch
    print '-'
  else:
    print labels[clust.id] if labels else clust.id

  if clust.left: printclust(clust.left, labels=labels, n=n+1)
  if clust.right: printclust(clust.right, labels=labels, n=n+1)


def transpose(data):
  return map(list, zip(*data))


# XXX: break into smaller pieces, test them
def kcluster(rows, distance=pearson_dist, k=4):
  # Our points are the columns (words in the example) of our data matrix.
  # Compute bounding box of points (in len(rows)-dimensional space)
  ranges = zip(map(min, transpose(rows)), map(max, transpose(rows)))

  clusters = [[random.uniform(r[0], r[1]) for r in ranges] for j in range(k)]

  lastmatches = None
  for t in range(100):
    print 'Iteration', t
    bestmatches = [[] for i in range(k)]

    # find best centroid for each row
    for j in range(len(rows)):
      row = rows[j]
      bestmatch = 0
      for i in range(k):
        d = distance(clusters[i], row)
        if d < distance(clusters[bestmatch], row): bestmatch = i
      bestmatches[bestmatch].append(j)
      
    # if the results didn't change in this iteration, we are done
    if bestmatches == lastmatches: break
    lastmatches = bestmatches

    # move centroids to the averages of their elements
    for i in range(k):
      avgs = [0.0] * len(rows[0])
      if len(bestmatches[i]) > 0:
        for rowid in bestmatches[i]:
          for m in range(len(rows[rowid])):
            avgs[m] += rows[rowid][m]
        for j in range(len(avgs)):
          avgs[j] /= len(bestmatches[i])
        clusters[i] = avgs

  return bestmatches


if __name__ == '__main__':
  import drawclust
  blognames, words, data = readfile('blogdata.txt')
  c = hcluster(data)
  #printclust(c, labels=blognames)
  drawclust.drawdendogram(c, blognames, 'dendo.png')
  print 'Wrote dendo.png'

  ## this is _much_ slower, as hcluster computes O(rows^2) many distances,
  ## and there are many more words than blognames in out data.
  #c = hcluster(transpose(data))
  #drawclust.drawdendogram(c, words, 'dendo_words.png')
  #print 'Wrote dendo_words.png'
