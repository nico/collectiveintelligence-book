import collections
import math
import operator
import re


def getwords(doc):
  splitter = re.compile(r'\W*')
  words = [s.lower() for s in splitter.split(doc) if 2 < len(s) < 20]
  return set(words)


class classifier(object):

  def __init__(self, getfeatures, filename=None):
    # Counts of ofeature/category combinations
    self.fc = collections.defaultdict(lambda: collections.defaultdict(int))

    # Counts of documents in each category
    self.cc = collections.defaultdict(int)
    self.getfeatures = getfeatures

  def incf(self, f, cat):
    self.fc[f][cat] += 1

  def incc(self, cat):
    self.cc[cat] += 1

  def fcount(self, f, cat):
    if f in self.fc and cat in self.fc[f]:
      return float(self.fc[f][cat])
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

  def cprob(self, cat):
    """Returns P(cat)."""
    if self.totalcount() == 0: return 0.0
    return self.catcount(cat) / self.totalcount()

  def fprob(self, f, cat):
    """Returns P(f | cat), i.e. chance that a document in category cat contains
    the given feature."""
    if self.catcount(cat) == 0: return 0.0
    return self.fcount(f, cat)/self.catcount(cat)

  def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
    """Returns guess for P(f | cat). The guess starts near `ap` if only few
    data is known."""
    basicprob = prf(f, cat)

    # Count how often this feature has occurred in any category
    totals = sum([self.fcount(f, c) for c in self.categories()])

    weightedp = ((weight*ap) + (totals*basicprob))/(weight + totals)
    return weightedp


class naivebayes(classifier):

  def docprob(self, doc, cat):
    """Returns P(doc | cat), assuming all words in doc are independent (which
    is not true, hence this does not really return a probability. The result is
    still useful, though)."""
    features = self.getfeatures(doc)
    probs = [self.weightedprob(f, cat, self.fprob) for f in features]
    return reduce(operator.mul, probs, 1.0)

  def prob(self, cat, doc):
    """Returns P(cat | doc), with the same caveats as listed for docprob().
    Also omits the division by P(doc), which would be required by Bayes's
    Theorem -- we don't care about that term."""
    # XXX: work out (on paper) what this does in terms of catcount etc
    return self.docprob(doc, cat) * self.cprob(cat)


def sampletrain(cl):
  cl.train('Nobody owns the water.', 'good')
  cl.train('the quick rabbit jumps fences', 'good')
  cl.train('buy pharmaceuticals now', 'bad')
  cl.train('make quick money at the online casino', 'bad')
  cl.train('the quick brown fox jumps', 'good')


if __name__ == '__main__':
  cl = classifier(getwords)
  sampletrain(cl)
  print cl.fcount('quick', 'good')
  print cl.fcount('quick', 'bad')
