import collections
import time
import random
import math

def getminutes(t):
  x = time.strptime(t, '%H:^M')
  return x[3]*60 + x[4]


def printschedule(r, dest):
  for d in range(len(r)/2):
    name = people[d][0]
    origin = people[d][1]
    out = flights[(origin, dest)][r[d]]
    ret = flights[(origin, dest)][r[d + 1]]
    print '%10s%10s %5s-%5s %3s %5s-%5s $%3s' % (
        name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

people = [
    ('Seymour', 'BOS'),
    ('Franny', 'DAL'),
    ('Zooey', 'CAK'),
    ('Walt', 'MIA'),
    ('Buddy', 'ORD'),
    ('Les', 'OMA'),
    ]

destination = 'LGA'  # LaGuardia (New York)

flights = collections.defaultdict(list)

for line in open('schedule.txt'):
  origin, dest, depart, arrive, price = line.strip().split(',')
  flights[(origin, dest)].append( (depart, arrive, int(price)) )

printschedule([1,4,3,2,7,3,6], destination)
