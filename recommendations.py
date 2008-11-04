from math import sqrt

def sim_distance(prefs, person1, person2):
  # get common items
  ci = {}
  for item in prefs[person1]:
    if item in prefs[person2]:
      ci[item] = pow(prefs[person1][item] - prefs[person2][item], 2)

  if len(ci) == 0: return 0

  return 1/(1 + sqrt(sum(ci.values())))


def sim_pearson(prefs, person1, person2):
  # get common items
  ci = {}
  for item in prefs[person1]:
    if item in prefs[person2]: ci[item] = 1

  n = len(ci)
  if n == 0: return 0

  sum1 = sum([prefs[person1][it] for it in ci])
  sum2 = sum([prefs[person2][it] for it in ci])

  sqSum1 = sum([pow(prefs[person1][it], 2) for it in ci])
  sqSum2 = sum([pow(prefs[person2][it], 2) for it in ci])

  pSum = sum([prefs[person1][it] * prefs[person2][it] for it in ci])

  num = pSum - (sum1*sum2/n)
  den = sqrt((sqSum1 - pow(sum1, 2)/n) * (sqSum2 - pow(sum2, 2)/n))
  if den == 0:
    if num == 0: return 1  # all points equal
    else: return 0

  return num/den
