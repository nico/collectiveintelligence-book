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


def printsolution(vec):
  slots = []
  for i in range(len(dorms)): slots += [i, i]

  for i in range(len(vec)):
    x = vec[i]
    print prefs[i][0], dorms[slots[x]]
    del slots[x]


if __name__ == '__main__':
  printsolution([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
