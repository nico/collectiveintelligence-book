import numpredict

from pylab import *

def cumulativegraph(data, vec1, high, k=5, weightfun=numpredict.gaussianweight):
  t1 = arange(0.0, high, 1)
  cprob = array([numpredict.probguess(data, vec1, 0, v, k, weightfun)
    for v in t1])
  plot(t1, cprob)
  show()  # this does user interaction

if __name__ == '__main__':
  s = numpredict.wineset3(k=500)

  # Draw graph that shows p(price | [rating=99, age=20])
  print 'Real price 1:', numpredict.wineprice(99.0, 20.0)
  print 'Real price 2:', 0.6 * numpredict.wineprice(99.0, 20.0)
  cumulativegraph(s, [99.0, 20.0], 120)
