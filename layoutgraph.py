import math

# Idea: first use optimization to create a layout with few intersections.
# Then a mass-spring model could be used to produce nice distances.

People=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

Links=[('Augustus', 'Willy'), 
       ('Mike', 'Joe'), 
       ('Miranda', 'Mike'), 
       ('Violet', 'Augustus'), 
       ('Miranda', 'Willy'), 
       ('Charlie', 'Mike'), 
       ('Veruca', 'Joe'), 
       ('Miranda', 'Augustus'), 
       ('Willy', 'Augustus'), 
       ('Joe', 'Charlie'), 
       ('Veruca', 'Augustus'), 
       ('Miranda', 'Joe')]


def solutiontodict(v, people):
  return dict([(people[i], (v[i*2], v[i*2 + 1])) for i in range(len(people))])


def testintersect(l1, l2):
  """Returns if two lines intersect. Parallel lines count as intersection if
  they overlap in more than one point. Lines touching at their end points do
  not count as intersection."""
  (x1, y1), (x2, y2) = l1
  (x3, y3), (x4, y4) = l2

  den = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)

  # XXX: if den is 0, then lines are parallel (possibly identical)
  if den == 0: return False

  ua = ((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3)) / float(den)
  ub = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)) / float(den)
  return 0 < ua < 1 and 0 < ub < 1


def cross(p1, p2):
  return p1[0]*p2[1] - p1[1]*p2[0]


def vec_length(p):
  return math.sqrt(p[0]*p[0] + p[1]*p[1])


def vec_angle(p1, p0, p2):
  d1 = (p1[0] - p0[0], p1[1] - p0[1])
  d2 = (p2[0] - p0[0], p2[1] - p0[1])
  c = cross(d1, d2)
  a = math.asin(c/vec_length(d1)/vec_length(d2))
  return a / math.pi * 180


def makecost(people, links):
  def crosscost(v):
    """Returns a cost based on line crossing count, people distance, and
    line angle."""
    loc = solutiontodict(v, people)
    cost = 0

    # Count line crossings
    # O(n^2) - don't use with large (>= 10000 links) input!
    for i in range(len(links)):
      for j in range(i+1, len(links)):
        l1 = loc[links[i][0]], loc[links[i][1]]
        l2 = loc[links[j][0]], loc[links[j][1]]

        if testintersect(l1, l2):
          cost += 1

    # Assign a cost to small angles
    for i in range(len(people)):
      points = []
      for j in range(len(links)):
        if links[j][0] == people[i]:
          points.append(links[j][1])
        elif links[j][1] == people[i]:
          points.append(links[j][0])
        else: continue

      p0 = loc[people[i]]
      for j in range(len(points)):
        for k in range(j+1, len(points)):
          p1 = loc[points[j]]
          p2 = loc[points[k]]
          angle = vec_angle(p1, p0, p2)
          if angle < 30:
            cost += 0.4*(1.0 - angle/30.0)

    # Distribute people evenly by assigning a cost to near people
    for i in range(len(people)):
      for j in range(i+1, len(people)):
        (x1, y1), (x2, y2) = loc[people[i]], loc[people[j]]
        dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if dist < 50:
          cost += 1.0 - dist/50.0

    print cost
    return cost
  return crosscost


if __name__ == '__main__':
  import optimization
  domain = [(10, 370)] * (len(People) * 2)
  f = makecost(People, Links)
  s = optimization.annealingoptimize(domain, f, step=50, cool=0.99)
  print f(s)
  print s
