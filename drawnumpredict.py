import numpredict

from pylab import *

S = 1.0

def cumulativegraph(data, vec1, high, k=5, weightfun=numpredict.gaussianweight):
  t1 = arange(0.0, high, S)
  cprob = array([numpredict.probguess(data, vec1, 0, v, k, weightfun)
    for v in t1])
  plot(t1, cprob)


def probabilitygraph(data, vec1, high, k=5, weightfun=numpredict.gaussianweight,
    ss=5.0/10):
  t1 = arange(0.0, high, S)
  probs = [numpredict.probguess(data, vec1, v, v+S, k, weightfun) for v in t1]

  # gaussian smooth with nearby points
  smoothed = []
  for i in range(len(probs)):  # O(n^2)
    sv = 0.0
    for j in range(0, len(probs)):
      dist = abs(i - j)*0.1
      weight = numpredict.gaussianweight(dist, sigma=ss)
      sv += weight*probs[j]
    smoothed.append(sv)

  plot(t1, array(probs))
  plot(t1, array(smoothed))


if __name__ == '__main__':
  s = numpredict.wineset3(k=500)

  import pprint
  pprint.pprint(s)

  #wine = [99.0, 20.0]  # choose params were the sample data is somewhat dense
  wine = [99.0, 20.0]  # choose params were the sample data is somewhat dense
  # Draw graph that shows p(price | wine)
  print 'Real price 1:', numpredict.wineprice(wine[0], wine[1])
  print 'Real price 2:', 0.6 * numpredict.wineprice(wine[0], wine[1])
  cumulativegraph(s, wine, 120)
  probabilitygraph(s, wine, 120)
  show()  # this does user interaction
