import unittest

import docclass

class GetwordsTest(unittest.TestCase):

  def testStripDuplicates(self):
    self.assertEquals(['mail', 'spam'],
        sorted(list(docclass.getwords('spam mail spam'))))


class Test(unittest.TestCase):

  def testX(self):

    cl = docclass.classifier(docclass.getwords)
    cl.train('spam spam spam', 'bad')
    self.assertEquals(1.0, cl.fprob('spam', 'bad'))


if __name__ == '__main__':
  unittest.main()
