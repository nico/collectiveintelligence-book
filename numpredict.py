import math
import random

import clusters


def wineprice(rating, age):
  peak_age = rating - 50

  price = rating/2
  if age > peak_age:
    price = price * (5 - (age - peak_age))
  else:
    price = price * (5 * ((age + 1)/peak_age))
  return max(0, price)


def wineset1(k=300):
  rows = []
  for i in range(k):
    rating = random.random()*50 + 50
    age = random.random() * 50
    price = wineprice(rating, age) * (random.random()*0.4 + 0.8)
    rows.append({'input': (rating, age), 'result': price})
  return rows


def wineset2(k=300):
  rows = []
  for i in range(k):
    rating = random.random()*50 + 50
    age = random.random() * 50
    aisle = float(random.randint(1, 20))
    bottlesize = [375.0, 750.0, 1500.0, 3000.0][random.randint(0, 3)]
    price = wineprice(rating, age) * (random.random()*0.4 + 0.8)

    # XXXP179: "less noise": Not really, text has 0.9*r + 0.2, that's _more_
    # noise?

    price *= bottlesize / 750
    rows.append({'input': (rating, age, aisle, bottlesize), 'result': price})
  return rows


def wineset3(k=300):
  rows = wineset1(k)
  for row in rows:
    if random.random() < 0.5:
      row['result'] *= 0.6  # "discount price", to simulate uneven distribution
  return rows


euclidean = clusters.euclid_dist


def getdistances(data, vec1):
  distancelist = map(lambda v: euclidean(vec1, v['input']), data)
  return sorted(zip(distancelist, range(len(data))))


def knnestimate(data, vec1, k=3):
  return weightedknn(data, vec1, k=k, weightfun=lambda d:1.0)


def inverseweight(dist, num=1.0, const=0.1):
  return num/(dist + const)


def subtractweight(dist, const=1.0):
  # Returns 0 for items with no neighbors within `dist`
  return max(0, const - dist)


#def gaussianweight(dist, sigma=10.0):
def gaussianweight(dist, sigma=5.0):
  return math.exp(-0.5 * (dist/sigma)**2)


def weightedknn(data, vec1, k=3, weightfun=gaussianweight):
  # Compute all n distances, but then only use k. What the hell.
  dlist = getdistances(data, vec1)

  avg = 0.0
  totalweight = 0.0
  for i in range(k):
    dist, idx = dlist[i]
    weight = weightfun(dist)
    avg += weight * data[idx]['result']
    totalweight += weight
  avg /= totalweight
  return avg


def partition(l, pred):
  """Paritions a list into to lists, based on a binary predicate."""
  flist, tlist = [], []
  for row in l:
    (tlist if pred(row) else flist).append(row)
  return flist, tlist


def dividedata(data, pTest=0.05):
  # The approach used in the book doesn't has some variation in the size
  # of the testset (sometimes the test set has 0 elements!), so use a
  # different approach instead
  #return partition(data, lambda r: random.random() < pTest)
  n = len(data)
  nTest = int(n*pTest)
  shuffledData = data[:]
  random.shuffle(shuffledData)
  return shuffledData[0:n-nTest], shuffledData[n-nTest:n]


def testalgorithm(algfun, trainset, testset):
  error = 0.0
  for row in testset:
    guess = algfun(trainset, row['input'])
    error += (row['result'] - guess)**2
  return error / len(testset)


def crossvalidate(algfun, data, trials=100, pTest=0.05):
  error = 0.0
  for i in range(trials):
    trainset, testset = dividedata(data, pTest)
    error += testalgorithm(algfun, trainset, testset)
  return error / trials


def rescale(data, scale):
  scaledata = []
  for row in data:
    scaled = [scale[i]*row['input'][i] for i in range(len(scale))]
    scaledata.append({'input':scaled, 'result':row['result']})
  return scaledata


def createcostfunction(algfun, data):
  def costf(scale):
    print scale
    sdata = rescale(data, scale)
    return crossvalidate(algfun, sdata, trials=100)
  return costf


def probguess(data, vec1, low, high, k=5, weightfun=gaussianweight):
  """Returns the probability that the result for input vec1 is in the
  interval [low, hight], based on the trainingdata data."""
  dlist = getdistances(data, vec1)
  nweight = 0.0  # weight of neighbors in interval
  tweight = 0.0  # weight of all neighbors ("total weight")

  for i in range(k):
    dist = dlist[i][0]
    idx = dlist[i][1]
    weight = weightfun(dist)
    v = data[idx]['result']

    if low <= v <= high:
      nweight += weight
    tweight += weight
  if tweight == 0.0: return 0.0
  return nweight / tweight


if __name__ == '__main__':
  s = wineset1(50)

  print knnestimate(s, (95.0, 3.0), k=1)
  print knnestimate(s, (95.0, 3.0), k=3)
  print knnestimate(s, (95.0, 3.0), k=5)
  print weightedknn(s, (95.0, 3.0), k=3)
  print wineprice(95.0, 3.0)

  print crossvalidate(knnestimate, s)
  print crossvalidate(lambda d, v: knnestimate(d, v, k=1), s)
  print crossvalidate(lambda d, v: knnestimate(d, v, k=5), s)
  print crossvalidate(lambda d, v: knnestimate(d, v, k=7), s)
  print crossvalidate(lambda d, v: weightedknn(d, v, k=5), s)

  # Use optimization to automatically rescale different dimensions
  print
  print 'set 2, not-to-scale parameters (XXX buggy, broken, incomplete)'
  s = wineset2(50)
  print crossvalidate(knnestimate, s)
  print crossvalidate(knnestimate, rescale(s, [10, 10, 0, 0.5]))

  # automatically figure out rescaling parameters. This runs forever.
  # And my optimization code might be broken, this recomputes the same
  # values over and over again. I should cache them. And fix broken stuff. (XXX)
  #import optimization
  #print optimization.annealingoptimize([(0, 20)] * 4,
      #createcostfunction(knnestimate, s), step=2)

  # This shows that tracking distributions is worthwile
  print
  print 'set 3, uneven distribution'
  s = wineset3()
  print probguess(s, [99, 20], 20, 120)
  print probguess(s, [99, 20], 120, 1000)
  print probguess(s, [99, 20], 40, 80)
  print probguess(s, [99, 20], 80, 120)
  print 'real price:', wineprice(99.0, 20.0)
  print 'estimated price:', weightedknn(s, [99.0, 20.0])
  print 'crossvalidation error:', crossvalidate(weightedknn, s)

