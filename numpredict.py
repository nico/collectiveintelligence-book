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


def wineset1():
  rows = []
  for i in range(300):
    rating = random.random()*50 + 50
    age = random.random() * 50
    price = wineprice(rating, age) * (random.random()*0.4 + 0.8)
    rows.append({'input': (rating, age), 'result': price})
  return rows


euclidean = clusters.euclid_dist


def getdistances(data, vec1):
  distancelist = map(lambda v: euclidean(vec1, v['input']), data)
  return sorted(zip(distancelist, range(len(data))))


def knnestimate(data, vec1, k=3):
  # Compute all n distances, but then only use k. What the hell.
  dlist = getdistances(data, vec1)

  avg = 0.0
  for i in range(k):
    idx = dlist[i][1]
    avg += data[idx]['result']
  avg /= k
  return avg


if __name__ == '__main__':
  s = wineset1()

  print knnestimate(s, (95.0, 3.0))
  print wineprice(95.0, 3.0)
