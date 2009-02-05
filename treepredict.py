import collections

class decisionnode(object):
  def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
    self.col = col  # colum index of value to test
    self.value = value  # reference value
    self.results = results  # stores results in leafs, empty for inner nodes
    self.tb = tb  # child on true branch
    self.fb = fb  # child on false branch


def divideset(rows, column, value):
  split_function = None
  if isinstance(value, int) or isinstance(value, float):
    split_function = lambda row: row[column] >= value
  else:
    split_function = lambda row: row[column] == value
    
  # There has to be a `partition` or `group` function somewhere
  set1 = [row for row in rows if split_function(row)]
  set2 = [row for row in rows if not split_function(row)]
  return (set1, set2)


def uniquecounts(rows):
  results = collections.defaultdict(int)
  for row in rows:
    # Result is last column
    r = row[len(row) - 1]
    results[r] += 1
  return results


def giniimpurity(rows):
  """Returns probability that a randomly placed item will end up in the wrong
  category. A low result means that stuff is categorized well."""
  total = len(rows)
  counts = uniquecounts(rows)
  imp = 0
  # O(n^2) in number of categories
  for k1 in counts:
    p1 = float(counts[k1])/total  # XXX: These loops can be written more nicely
    for k2 in counts:
      if k1 == k2: continue
      p2 = float(counts[k1])/total
      imp += p1*p2
  return imp


def entropy(rows):
  from math import log
  log2 = lambda x: log(x)/log(2)
  results = uniquecounts(rows)
  ent = 0.0
  for r in results:
    p = float(results[r])/len(rows)
    ent -= p*log2(p)
  return ent


def testdata():
  def cleanup(s):
    s = s.strip()
    try:
      return int(s)
    except ValueError:
      return s
  return [map(cleanup, line.split('\t'))
      for line in open('decision_tree_example.txt')]


if __name__ == '__main__':
  my_data=[['slashdot','USA','yes',18,'None'],
          ['google','France','yes',23,'Premium'],
          ['digg','USA','yes',24,'Basic'],
          ['kiwitobes','France','yes',23,'Basic'],
          ['google','UK','no',21,'Premium'],
          ['(direct)','New Zealand','no',12,'None'],
          ['(direct)','UK','no',21,'Basic'],
          ['google','USA','no',24,'Premium'],
          ['slashdot','France','yes',19,'None'],
          ['digg','USA','no',18,'None'],
          ['google','UK','no',18,'None'],
          ['kiwitobes','UK','no',19,'None'],
          ['digg','New Zealand','yes',12,'Basic'],
          ['slashdot','UK','no',21,'None'],
          ['google','UK','yes',18,'Basic'],
          ['kiwitobes','France','yes',19,'Basic']]

  my_data2 = testdata()

  print my_data == my_data2
  import pprint
  pprint.pprint(my_data)
  pprint.pprint(my_data2)
