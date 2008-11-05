from math import sqrt

import collections

# prefs is a map from people to a map from things to scores


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
    if num == 0: return 1  # all points equal. or: just one common item.
    else: return 0

  return num/den


def topMatches(prefs, person, n=5, similarity=sim_pearson):
  """Given a map from persons to personal preferences, returns the top n
  people similar to a given person."""

  scores = [(similarity(prefs, person, other), other)
      for other in prefs if other != person]
  scores.sort(reverse=True)
  return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
  totals = collections.defaultdict(int)
  simSums = collections.defaultdict(int)
  for other in prefs:
    if other == person: continue

    sim = similarity(prefs, person, other)
    if sim <= 0: continue

    for item in prefs[other]:
      # only score items person doesn't know
      if item not in prefs[person] or prefs[person][item] == 0:
        simSums[item] += sim
        totals[item] += prefs[other][item]*sim  # weight score by similarity

  # Note that renormalization gives items that are only known to one person
  # their score, regardless of how similar I am to them
  rankings = [(total/simSums[item], item) for item,total in totals.items()]
  return sorted(rankings, reverse=True)

