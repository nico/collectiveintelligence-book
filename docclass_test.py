import unittest

import docclass

class GetwordsTest(unittest.TestCase):

  def testStripDuplicates(self):
    self.assertEquals(['mail', 'spam'],
        sorted(list(docclass.getwords('spam mail spam'))))


class ClassifierTest(unittest.TestCase):

  def testBasic(self):
    cl = docclass.classifier(docclass.getwords)
    cl.train('spam spam spam', 'bad')
    self.assertEquals(1.0, cl.fprob('spam', 'bad'))


class NaivebayesTest(unittest.TestCase):

  def testBasic(self):
    cl = docclass.naivebayes(docclass.getwords)
    docclass.sampletrain(cl)
    self.assertAlmostEquals(0.15624999, cl.prob('good', 'quick rabbit'))
    self.assertAlmostEquals(0.05, cl.prob('bad', 'quick rabbit'))


if __name__ == '__main__':
  unittest.main()
