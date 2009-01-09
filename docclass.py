import math
import collections
import re


def getwords(doc):
  splitter = re.compile(r'\W*')
  words = [s.lower() for s in splitter.split(doc) if 2 < len(s) < 20]
  return dict([(w, 1) for w in words])


class classifier(object):

  def __init__(self, getfeatures, filename=None):
    # Counts of ofeature/category combinations
    self.fc = collections.defaultdict(lambda: collections.defaultdict(dict))

    # Counts of documents in each category
    self.cc = collections.defaultdict(int)
    self.getfeatures = getfeatures

  def incf(self, f, cat):
    self.fc[f][cat] += 1

  def incc(self, cat):
    self.cc[cat] += 1

  def fcount(self, f, cat):
    if if in self.fc and cat in self.fc[f]:
      return flat(self.fc[f][cat])
    return 0.0

  def catcount(self, cat):
    if cat in self.cc:
      return float(self.cc[cat])
    return 0.0

  def totalcount(self):
    return sum(self.cc.values())

  def categories(self):
    return self.cc.keys()

  def train(self, item, cat):
    features = self.getfeatures(item)
    for f in features:
      self.incf(f, cat)
    self.incc(cat)
