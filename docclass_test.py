import unittest

import docclass

class GetwordsTest(unittest.TestCase):

  def testStripDuplicates(self):
    self.assertEquals(['mail', 'spam'],
        sorted(list(docclass.getwords('spam mail spam'))))


class ClassifierTest(unittest.TestCase):

  def testBasic(self):
    cl = docclass.classifier(docclass.getwords)
    cl.setdb('test.db')
    cl.train('spam spam spam', 'bad')
    self.assertEquals(1.0, cl.fprob('spam', 'bad'))


class NaivebayesTest(unittest.TestCase):

  def testProb(self):
    cl = docclass.naivebayes(docclass.getwords)
    cl.setdb('test.db')
    docclass.sampletrain(cl)
    self.assertAlmostEquals(0.15624999, cl.prob('good', 'quick rabbit'))
    self.assertAlmostEquals(0.05, cl.prob('bad', 'quick rabbit'))

  def testClassify(self):
    cl = docclass.naivebayes(docclass.getwords)
    cl.setdb('test.db')
    docclass.sampletrain(cl)
    self.assertEquals('good', cl.classify('quick rabbit', default='unknown'))
    self.assertEquals('bad', cl.classify('quick money', default='unknown'))

    cl.setthreshold('bad', 3.0)
    self.assertEquals('unknown', cl.classify('quick money', default='unknown'))

    for i in range(10): docclass.sampletrain(cl)
    self.assertEquals('bad', cl.classify('quick money', default='unknown'))


class FisherclassifierTest(unittest.TestCase):

  def testProb(self):
    cl = docclass.fisherclassifier(docclass.getwords)
    cl.setdb('test.db')
    docclass.sampletrain(cl)
    self.assertAlmostEquals(0.57142857, cl.cprob('quick', 'good'))
    self.assertAlmostEquals(0.78013987, cl.fisherprob('quick rabbit', 'good'))
    self.assertAlmostEquals(0.35633596, cl.fisherprob('quick rabbit', 'bad'))

  def testClassify(self):
    cl = docclass.fisherclassifier(docclass.getwords)
    cl.setdb('test.db')
    docclass.sampletrain(cl)

    self.assertEquals('good', cl.classify('quick rabbit', default='unknown'))
    self.assertEquals('bad', cl.classify('quick money', default='unknown'))

    cl.setminimum('bad', 0.8)
    self.assertEquals('good', cl.classify('quick money', default='unknown'))

    cl.setminimum('bad', 0.4)
    self.assertEquals('bad', cl.classify('quick money', default='unknown'))

  def testOneCategory(self):
    cl = docclass.fisherclassifier(docclass.getwords)
    cl.setdb('test.db')
    cl.train('hallo hallo', 'greeting')
    self.assertEquals('greeting', cl.classify('hallo world'))


if __name__ == '__main__':
  unittest.main()
