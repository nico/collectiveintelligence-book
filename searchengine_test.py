import unittest

import searchengine

class CrawlerTest(unittest.TestCase):

  def setUp(self):
    self.c = searchengine.crawler('')

  def testSeparatewords(self):
    self.assertEquals(['hi', 'how', 'are', 'you'],
        self.c.separatewords(' Hi, hOw.  arE! you? '))

if __name__ == '__main__':
  unittest.main()
