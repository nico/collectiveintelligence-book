import os
import re
import urllib2
import urlparse

from pysqlite2 import dbapi2 as sqlite
from BeautifulSoup import BeautifulSoup


ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


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
    pass

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
    sql, wordids = self.getmatchquery(q)
    print sql
    cur = self.con.execute(sql)
    rows = list(cur)
    return rows, wordids

  def getscoredlist(self, rows, wordids):
    totalscores = dict([(row[0], 0) for row in rows])

    weights = []

    for weight, scores in weights:
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


if __name__ == '__main__':
  create = not os.path.exists('searchindex.db')
  crawl = crawler('searchindex.db')
  if create:
    crawl.createindextables()

  if False:
    crawl.crawl(['http://amnoid.de/'], depth=3)

  s = searcher('searchindex.db')
  print s.getmatchrows('ddsview is great')
