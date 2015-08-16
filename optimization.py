import collections
import time
import random
import math


def getminutes(t):
  x = time.strptime(t, '%H:%M')
  return x[3]*60 + x[4]


def parseCsv(lines):
  flights = collections.defaultdict(list)
  for line in lines:
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights[(origin, dest)].append( (depart, arrive, int(price)) )
  return flights


def printschedule(r, dest):
  for d in range(len(r)/2):
    name = people[d][0]
    origin = people[d][1]
    out = flights[(origin, dest)][r[d]]
    ret = flights[(origin, dest)][r[d + 1]]
    print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (
        name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])


def costfunc(flights, dest):
  def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60

    for d in range(len(sol) // 2):
      origin = people[d][1]
      outbound = flights[(origin, dest)][int(sol[d])]
      returnf = flights[(dest, origin)][int(sol[d+1])]

      totalprice += outbound[2] + returnf[2]

      latestarrival = max(latestarrival, getminutes(outbound[1]))
      earliestdep = min(latestarrival, getminutes(returnf[0]))

    # Every person must wait until the last person arrives.
    # They must also arrive when the first flight leaves
    totalwait = 0
    for d in range(len(sol)/2):
      origin = people[d][1]
      outbound = flights[(origin, dest)][int(sol[d])]
      returnf = flights[(dest, origin)][int(sol[d+1])]
      totalwait += latestarrival - getminutes(outbound[1])
      totalwait += getminutes(returnf[0]) - earliestdep

    # One additional day of car rental fees?
    if latestarrival >= earliestdep: totalprice += 50

    return totalprice + totalwait
  return schedulecost


def randomoptimize(domain, costf):
  best = 99999999
  bestr = None
  for i in range(1000):
    r = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]
    cost = costf(r)
    if cost < best:
      best = cost
      bestr = r
  return r


def hillclimbopt(domain, costf):
  sol = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]

  while True:
    neighbors = []
    for j in range(len(domain)):
      if sol[j] > domain[j][0]:
        neighbors.append(sol[0:j] + [sol[j] - 1] + sol[j + 1:])
      if sol[j] < domain[j][1]:
        neighbors.append(sol[0:j] + [sol[j] + 1] + sol[j + 1:])

    current = costf(sol)
    best = current
    for j in range(len(neighbors)):
      cost = costf(neighbors[j])
      if cost < best:
        best = cost
        sol = neighbors[j]

    if best == current:
      break
  return sol


def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step=1):
  sol = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]

  while T > 0.1:
    # Create disturbed solution
    i = random.randint(0, len(domain)-1)
    dir = random.randint(-step, step)
    solb = sol[:]
    solb[i] += dir
    solb[i] = max(solb[i], domain[i][0])
    solb[i] = min(solb[i], domain[i][1])

    # Compare costs
    ca = costf(sol)
    cb = costf(solb)
    p = math.exp(-(ca + cb)/T)

    # Accept all better solutions, accept worse one depending on temperature
    if cb < ca or random.random() < p:
      sol = solb

    T *= cool
  return sol


def geneticoptimize(domain, costf, popsize=50, step=1,
    mutprob=0.2, elite=0.2, maxiter=100):
  def mutate(vec):
    assert len(domain) == len(vec)
    i = random.randint(0, len(domain)-1)
    # XXX: broken.
    # 1. step not in range check
    # 2. prob and bounds check mixed up
    if random.random() < 0.5 and vec[i] > domain[i][0]:
      return vec[0:i] + [max(vec[i] - step, domain[i][0])] + vec[i+1:]
    elif vec[i] < domain[i][1]:
      return vec[0:i] + [min(vec[i] + step, domain[i][1])] + vec[i+1:]
    elif vec[i] == domain[i][1]:
      return vec[0:i] + [max(vec[i] - step, domain[i][0])] + vec[i+1:]

  def crossover(r1, r2):
    i = random.randint(1, len(domain)-2)
    return r1[0:i] + r2[i:]

  # Starting population
  pop = [[random.randint(domain[j][0],domain[j][1])
    for j in range(len(domain))]
    for i in range(popsize)]

  numWinners = int(elite*popsize)
  for i in range(maxiter):
    ranked = sorted(pop, key=costf)

    # add winners
    pop = ranked[0:numWinners]

    # add mutated and bred forms of the winners
    while len(pop) < popsize:
      if random.random() < mutprob:
        newGuy = mutate(ranked[random.randint(0, numWinners-1)])
      else:
        newGuy = crossover(ranked[random.randint(0, numWinners-1)],
          ranked[random.randint(0, numWinners-1)])
      if not newGuy:
        print i, numWinners, len(pop)
        raise "omg"
      pop.append(newGuy)

    # Print current best score
    print costf(ranked[0])

  # Return current best guy
  return ranked[0]


if __name__ == '__main__':
  people = [
      ('Seymour', 'BOS'),
      ('Franny', 'DAL'),
      ('Zooey', 'CAK'),
      ('Walt', 'MIA'),
      ('Buddy', 'ORD'),
      ('Les', 'OMA'),
      ]

  destination = 'LGA'  # LaGuardia (New York)

  flights = parseCsv(open('schedule.txt'))

  # 10 flights in each direction
  #for f in flights:
    #print f, len(flights[f])

  f = costfunc(flights, destination)
  domain = [(0, 8)] * (len(people) * 2)

  r = randomoptimize(domain, f)
  printschedule(r, destination)
  print f(r)

  r = hillclimbopt(domain, f)
  printschedule(r, destination)
  print f(r)

  r = annealingoptimize(domain, f)
  printschedule(r, destination)
  print f(r)

  r = geneticoptimize(domain, f)
  printschedule(r, destination)
  print f(r)
