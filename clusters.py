from math import sqrt


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
    if num == 0: return 1  # all points equal. or: just one common item.
    else: return 0

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
