import feedparser
import re


def interestingwords(s):
  splitter = re.compile(r'\W*')
  return [s.lower() for s in splitter.split(s) if len(s) > 2 and len(s) < 20]


def entryfeatures(entry):
  f = {}

  # extract title
  titlewords = interestingwords(entry['title'])
  for w in titlewords: f['Title:' + w] = 1

  # extract summary
  summarywords = interestingwords(entry['summary'])

  # count uppercase words
  uc = 0
  for i in range(len(summarywords)):
    w = summarywords[i]
    f[w] = 1
    if w.isupper(): uc += 1

    # get word pairs in summary aas features
    if i < len(summarywords) - 1:
      twowords = ' '.join(summarywords[i:i+1])
      f[twowords] = 1

  # keep creator and publisher as a whole
  f['Publisher:' + entry['publisher']] = 1

  # Insert virtual keyword for uppercase words
  if float(uc) / len(summarywords) > 0.3: f['UPPERCASE'] = 1

  print f.keys()
  return f.keys()


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

    #print 'Guess: ' + str(classifier.classify(fulltext))

    #cl = raw_input('Enter category: ')
    #classifier.train(fulltext, cl)

    print 'Guess: ' + str(classifier.classify(entry))

    cl = raw_input('Enter category: ')
    classifier.train(entry, cl)


if __name__ == '__main__':
  import docclass

  #cl = docclass.fisherclassifier(docclass.getwords)
  cl = docclass.fisherclassifier(entryfeatures)
  cl.setdb('python_feed.db')
  read('python_search.xml', cl)
