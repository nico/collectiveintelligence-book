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
