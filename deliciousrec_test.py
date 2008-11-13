import unittest

import deliciousrec


class BuildTagsListTest(unittest.TestCase):

  def testBasics(self):

    d = {
      'thakis': [{'href': 'amnoid.de', 'tags': 'this is nice'},
                 {'href': 'bar.com', 'tags': ''},
                 {'href': 'bla.com', 'tags': 'bla'}],
      'ytamshg': [{'href': 'amnoid.de', 'tags': 'wtf is this shit'},
                  {'href': 'bla.com', 'tags': ''},
                  {'href': 'foo.de', 'tags': 'bla'}]
    }

    expected = {
      'this': {'amnoid.de': 2.0},
      'is': {'amnoid.de': 2.0},
      'nice': {'amnoid.de': 1.0},
      'bla': {'bla.com': 1.0, 'foo.de':1.0},
      'wtf': {'amnoid.de': 1.0},
      'shit': {'amnoid.de': 1.0},
    }

    print deliciousrec.buildTagsList(d)
    self.assertEquals(expected, deliciousrec.buildTagsList(d))
       

if __name__ == '__main__':
  unittest.main()

