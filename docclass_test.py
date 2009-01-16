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

  def testProb(self):
    cl = docclass.naivebayes(docclass.getwords)
    docclass.sampletrain(cl)
    self.assertAlmostEquals(0.15624999, cl.prob('good', 'quick rabbit'))
    self.assertAlmostEquals(0.05, cl.prob('bad', 'quick rabbit'))

  def testClassify(self):
    cl = docclass.naivebayes(docclass.getwords)
    docclass.sampletrain(cl)
    self.assertEquals('good', cl.classify('quick rabbit', default='unknown'))
    self.assertEquals('bad', cl.classify('quick money', default='unknown'))

    cl.setthreshold('bad', 3.0)
    self.assertEquals('unknown', cl.classify('quick money', default='unknown'))

    for i in range(10): docclass.sampletrain(cl)
    self.assertEquals('bad', cl.classify('quick money', default='unknown'))


if __name__ == '__main__':
  unittest.main()
