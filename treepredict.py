
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


if __name__ == '__main__':
  my_data = [line.split('\t') for line in open('decision_tree_example.txt')]
