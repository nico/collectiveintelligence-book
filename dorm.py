import math
import random

dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']

prefs=[('Toby', ('Bacchus', 'Hercules')),
       ('Steve', ('Zeus', 'Pluto')),
       ('Karen', ('Athena', 'Zeus')),
       ('Sarah', ('Zeus', 'Pluto')),
       ('Dave', ('Athena', 'Bacchus')), 
       ('Jeff', ('Hercules', 'Pluto')), 
       ('Fred', ('Pluto', 'Athena')), 
       ('Suzie', ('Bacchus', 'Hercules')), 
       ('Laura', ('Bacchus', 'Hercules')), 
       ('James', ('Hercules', 'Athena'))]

# [(0, 9), (0, 8), ... , (0, 1)]
domain = [(0, len(dorms)*2 - i - 1) for i in range(0, len(dorms)*2)]


def slotlist(l):
  slots = []
  for i in range(l): slots += [i, i]
  return slots


def printsolution(vec):
  slots = slotlist(len(dorms))
  for i in range(len(vec)):
    x = vec[i]
    print prefs[i][0], dorms[slots[x]]
    del slots[x]


def dormcost(vec):
  cost = 0
  slots = slotlist(len(dorms))
  for i in range(len(vec)):
    x = vec[i]

    dorm = dorms[slots[x]]
    pref = prefs[i][1]

    if pref[0] == dorm: cost += 0
    elif pref[1] == dorm: cost += 1
    else: cost += 3

    del slots[x]

  return cost


if __name__ == '__main__':
  printsolution([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

  import optimization
  s = optimization.geneticoptimize(domain, dormcost)
  printsolution(s)
