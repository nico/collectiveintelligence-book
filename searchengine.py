import os
import re
import urllib2
import urlparse

from pysqlite2 import dbapi2 as sqlite
from BeautifulSoup import BeautifulSoup

import nn
net = nn.searchnet('nn.db')  # XXX: somehow train this from user clicks

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


# XXX: the root page (amnoid.de) is indexed twice for some reason (e.g.
#   select * from links where toid = 2;
# shows the link 1->2 two times.
class crawler:

  def __init__(self, dbname):
    self.con = sqlite.connect(dbname)

  def __del__(self):
    self.con.close()

  def dbcommit(self):
    self.con.commit()

  def getentryid(self, table, field, value, createnew=True):
    """Returns an entry id and creates it if it is not present."""
    cur = self.con.execute('select rowid from %s where %s="%s"'
        % (table, field, value))
    result = cur.fetchone()
    if not result:
      cur = self.con.execute('insert into %s (%s) values("%s")'
          % (table, field, value))
      return cur.lastrowid
    else:
      return result[0]

  def addtoindex(self, url, soup):
    """Indexes a given page."""
    if self.isindexed(url): return
    print 'Indexing', url

    # Extract words
    text = self.gettextonly(soup)
    words = self.separatewords(text)

    # Get url id from db
    urlid = self.getentryid('urllist', 'url', url)

    # Link each word to that url
    for i in range(len(words)):
      word = words[i]
      if word in ignorewords: continue
      wordid = self.getentryid('wordlist', 'word', word)
      self.con.execute('insert into wordlocation(urlid, wordid, location) \
          values (%d, %d, %d)' % (urlid, wordid, i))

  def gettextonly(self, soup):
    """Extracts all text from a html page, i.e. strips the tags."""
    v = soup.string
    if v == None:
      return '\n'.join([self.gettextonly(t) for t in soup.contents])
    else:
      return v.strip()

  def separatewords(self, text):
    """Splits words by non-whitespace characters."""
    splitter = re.compile(r'\W*')
    return [s.lower() for s in splitter.split(text) if s != '']

  def isindexed(self, url):
    cur = self.con.execute('select rowid from urllist where url="%s"' % url)
    u = cur.fetchone()
    if not u: return False

    # check if it has been crawled (XXX: why?)
    v = self.con.execute('select * from wordlocation where urlid="%d"'
        % u[0]).fetchone()
    return v != None

  def addlinkref(self, urlfrom, urlto, linktext):
    """Add a link between two pages."""
    fromid = self.getentryid('urllist', 'url', urlfrom)
    toid = self.getentryid('urllist', 'url', urlto)
    if fromid == toid: return
    cur = self.con.execute('insert into link (fromid, toid) values (%d, %d)'
        % (fromid, toid))

    linkid = cur.lastrowid
    # Remember each word in link text
    for word in self.separatewords(linktext):
      if word in ignorewords: continue
      wordid = self.getentryid('wordlist', 'word', word)
      self.con.execute('insert into linkwords (wordid, linkid) \
          values (%d, %d)' % (wordid, linkid))


  def crawl(self, pages, depth=2):
    """Find pages linked from a root set in BFS order, up to a given depth."""
    for i in range(depth):
      newpages = set()
      for page in pages:
        try:
          print page
          c = urllib2.urlopen(page)
        except urllib2.URLError:
          print 'Could not load', page
          continue

        if c.headers.type not in set(['text/html', 'text/plain']):
          print 'Skipping', page, c.headers.type
          continue

        soup = BeautifulSoup(c.read())
        self.addtoindex(page, soup)

        links = soup.findAll('a')
        for link in links:
          if 'href' in dict(link.attrs):
            url = urlparse.urljoin(page, link['href'])
            if url.find("'") != -1:
              print 'IGNORING', url
              continue
            url = url.split('#')[0]
            if url[0:4] == 'http' and not self.isindexed(url):
              newpages.add(url)
            linktext = self.gettextonly(link)
            self.addlinkref(page, url, linktext)

        self.dbcommit()

      pages = newpages

  def createindextables(self):
    """Create the database tables."""
    self.con.execute('create table urllist(url)')
    self.con.execute('create table wordlist(word)')
    self.con.execute('create table wordlocation(urlid, wordid, location)')
    self.con.execute('create table link(fromid integer, toid integer)')
    self.con.execute('create table linkwords(wordid, linkid)')

    self.con.execute('create index urlidx on urllist(url)')
    self.con.execute('create index wordidx on wordlist(word)')
    self.con.execute('create index wordurlidx on wordlocation(wordid)')
    self.con.execute('create index urlfromidx on link(fromid)')
    self.con.execute('create index urltoidx on link(toid)')
    self.dbcommit()

  # XXX: If a page with a highish pagerank links 16 other pages, and one
  # of those links to just one page C, then C has a higher pagerank than
  # the original high-pr page. Weird.
  def calculatepagerank(self, iterations=20):
    self.con.execute('drop table if exists pagerank')
    self.con.execute('create table pagerank(urlid primary key, score)')

    # initialize all pageranks with 1.0 (actual value does not matter)
    self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
    self.dbcommit()

    for i in range(iterations):
      print 'Iteration', i
      for urlid, in self.con.execute('select rowid from urllist'):
        pr = 0.15

        # Loop through all pages that link to this one
        for linker, in self.con.execute(
            'select distinct fromid from link where toid = %d' % urlid):
          # Get pagerank of linker
          linkingrank = self.con.execute('select score from pagerank '
              + 'where urlid = %d' % linker).fetchone()[0]

          # Get total number of links on page 'linker'
          linkingcount = self.con.execute('select count(*) '
              + 'from link where fromid = %d' % linker).fetchone()[0]

          pr += 0.85 * (linkingrank / linkingcount)

        # Store pagerank
        self.con.execute(
            'update pagerank set score = %f where urlid = %d' % (pr, urlid))
      self.dbcommit()


class searcher:
  def __init__(self, dbname):
    self.con = sqlite.connect(dbname)

  def __del__(self):
    self.con.close()

  def getmatchquery(self, q):
    # Example query:
    # SELECT w0.urlid, w0.location, w1.location, w2.location 
    # FROM wordlocation w0, wordlocation w1, wordlocation w2 
    # WHERE w0.wordid = 255
    #       and w0.urlid = w1.urlid and w1.wordid = 1192
    #       and w1.urlid = w2.urlid and w2.wordid = 73

    # XXX: This returns O((n/k)^k) many results for a query with k known words
    #      (n is number of words on a page) for each page.

    # XXX: Break this into pieces, test them
    fieldlist = 'w0.urlid'
    tablelist = ''
    clauselist = ''
    wordids = []
    words = q.split(' ')
    tablecount = 0

    for word in words:
      wordrow = self.con.execute('select rowid from wordlist where word = "%s"'
          % word).fetchone()
      if not wordrow: continue
      wordid = wordrow[0]
      wordids.append(wordid)
      if tablecount > 0:
        tablelist += ', '
        clauselist += ' and '
        clauselist += 'w%d.urlid = w%d.urlid and ' % (
            tablecount - 1, tablecount)
      fieldlist += ', w%d.location' % tablecount
      tablelist += 'wordlocation w%d' % tablecount
      clauselist += 'w%d.wordid = %d' % (tablecount, wordid)
      tablecount += 1

    if tablecount == 0:
      return '', wordids

    fullquery = 'select %s from %s where %s' % (
        fieldlist, tablelist, clauselist)
    return fullquery, wordids

  def getmatchrows(self, q):
    """Returns list of tuples. 1st element of each tuple is urlid, the others
    are the positions of each query word in that document."""
    sql, wordids = self.getmatchquery(q)
    print sql
    cur = self.con.execute(sql)
    rows = list(cur)
    return rows, wordids

  def getscoredlist(self, rows, wordids):
    totalscores = dict([(row[0], 0) for row in rows])
    if not rows: return totalscores

    weightedScores = [(2.0, self.frequencyscore(rows)),
        (1.0, self.locationscore(rows)),
        (1.0, self.distancescore(rows)),
        (1.0, self.inboundlinkscore(rows)),
        (1.0, self.pagerankscore(rows)),
        (1.0, self.linktextscore(rows, wordids)),
        (0.0, self.nnscore(rows, wordids)),  # not trained yet...
        ]

    for weight, scores in weightedScores:
      for url in totalscores:
        totalscores[url] += weight * scores[url]

    return totalscores

  def geturlname(self, id):
    return self.con.execute(
        'select url from urllist where rowid = %d' % id).fetchone()[0]

  def query(self, q):
    rows, wordids = self.getmatchrows(q)
    scores = self.getscoredlist(rows, wordids)
    rankedscores = sorted([(score, url) for url, score in scores.items()],
      reverse=True)
    return [(score, self.geturlname(urlid))
        for (score, urlid) in rankedscores[0:10]]

  # Scoring functions

  def normalizescores(self, scores, smallIsBetter=False):
    vsmall = 0.00001  # smoothen out division by zero
    if smallIsBetter:
      minscore = min(scores.values())
      return dict([(u, float(minscore)/max(vsmall, l))
        for (u, l) in scores.items()])
    else:
      maxscore = max(scores.values())
      if maxscore == 0: maxscore = vsmall
      return dict([(u, float(c)/maxscore) for (u, c) in scores.items()])

  def frequencyscore(self, rows):
    counts = dict([(row[0], 0) for row in rows])

    # disproportionally high, see the "XXX" above
    for row in rows: counts[row[0]] += 1
    return self.normalizescores(counts, smallIsBetter=False)

  def locationscore(self, rows):
    locations = dict([(row[0], 1000000) for row in rows])
    for row in rows:
      loc = sum(row[1:])
      if loc < locations[row[0]]: locations[row[0]] = loc
    return self.normalizescores(locations, smallIsBetter=True)

  def distancescore(self, rows):
    # only one word in query?
    if len(rows[0]) <= 2: return dict([(row[0], 1.0) for row in rows])

    mindistance = dict([(row[0], 1000000) for row in rows])
    for row in rows:
      dist = sum([abs(row[i] - row[i - 1]) for i in range(2, len(row))])
      if dist < mindistance[row[0]]: mindistance[row[0]] = dist
    return self.normalizescores(mindistance, smallIsBetter=True)

  def inboundlinkscore(self, rows):
    uniqueurls = set([row[0] for row in rows])  # XXX: why is this needed?
    inboundcount = dict([(u, self.con.execute(
      'select count(*) from link where toid = %d' % u).fetchone()[0])
      for u in uniqueurls])
    return self.normalizescores(inboundcount, smallIsBetter=False)

  def pagerankscore(self, rows):
    pageranks = dict([(row[0], self.con.execute('select score from pagerank '
      + 'where urlid = %d' % row[0]).fetchone()[0]) for row in rows])
    return self.normalizescores(pageranks, smallIsBetter=False)

  def linktextscore(self, rows, wordids):
    linkscores = dict([(row[0], 0) for row in rows])
    for wordid in wordids:
      cur = self.con.execute(
          'select link.fromid, link.toid from linkwords, link '
        + 'where wordid = %d and linkwords.linkid = link.rowid' % wordid)
      for fromid, toid in cur:
        if toid in linkscores:
          rank = self.con.execute('select score from pagerank where urlid = %d'
              % fromid).fetchone()[0]
          linkscores[toid] += rank
    return self.normalizescores(linkscores, smallIsBetter=False)

  def nnscore(self, rows, wordids):
    # Get unique url ids as ordered list
    urlids = list(set([row[0] for row in rows]))
    #urlids = list(set([row[0] for row in rows]))
    #assert urlids == sorted(urlids)
    nnres = net.getresult(wordids, urlids)
    scores = dict([(urlids[i], nnres[i]) for i in range(len(urlids))])
    return self.normalizescores(scores, smallIsBetter=False)


if __name__ == '__main__':
  create = not os.path.exists('searchindex.db')
  crawl = crawler('searchindex.db')
  if create:
    crawl.createindextables()

  if True:
    crawl.crawl(['http://amnoid.de/'], depth=3)
    crawl.calculatepagerank()

  s = searcher('searchindex.db')
  print s.query('ddsview is great')
