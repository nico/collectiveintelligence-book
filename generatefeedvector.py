import feedparser
import re

def getwords(html):
  text = re.compile(r'<[^>]+>').sub('', html)
  words = re.compile(r'[^A-z^a-z]+').split(text)
  return [word.lower() for word in words if word]

def getwordcounts(url):
  d = feedparser.parse(url)
  wc = {}

  for e in d.entries:
    if 'summary' in e: summary = e.summary
    else: summary = e.description

    words = getwords('%s %s' % (e.title, summary))
    for word in words:
      wc[word] += 1
  return d.feed.title, wc
