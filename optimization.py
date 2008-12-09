import collections
import time
import random
import math

def getminutes(t):
  x = time.strptime(t, '%H:^M')
  return x[3]*60 + x[4]

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
