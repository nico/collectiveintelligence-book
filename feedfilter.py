import feedparser
import re

def read(feed, classifier):
  f = feedparser.parse(feed)
  for entry in f['entries']:
    print
    print '----'
    print 'Title:     ' + entry['title'].encode('utf-8')
    print 'Publisher: ' + entry['publisher'].encode('utf-8')
    print
    print entry['summary'].encode('utf-8')

    fulltext = '%s\n%s\n%s' % (
        entry['title'], entry['publisher'], entry['summary'])

    print 'Guess: ' + str(classifier.classify(fulltext))

    cl = raw_input('Enter category: ')
    classifier.train(fulltext, cl)


if __name__ == '__main__':
  import docclass

  cl = docclass.fisherclassifier(docclass.getwords)
  cl.setdb('python_feed.db')
  read('python_search.xml', cl)
