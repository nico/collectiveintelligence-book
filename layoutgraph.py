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


def makecost(people, links):
  def crosscount(v):
    """Returns number of crossing lines."""
    loc = dict([(people[i], (v[i*2], v[i*2 + 1])) for i in range(len(people))])
    count = 0

    # O(n^2) - don't use with large (>= 10000 links) input!
    for i in range(len(links)):
      for j in range(i+1, len(links)):

        (x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]]  # line 1
        (x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]]  # line 2

        den = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)

        # if den is 0, then lines are parallel (possibly identical)
        if den == 0: continue

        ua = ((x4 - x3)*(y1 - y2) - (y4 - y3)*(x1 - x3)) / float(den)
        ub = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)) / float(den)

        if 0 < ua < 1 and 0 < ub < 1:
          count += 1
    return count
  return crosscount


if __name__ == '__main__':
  import optimization
  domain = [(10, 370)] * (len(People) * 2)
  f = makecost(People, Links)
  s = optimization.annealingoptimize(domain, f, step=50, cool=0.99)
  print f(s)
  print s
