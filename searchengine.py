import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup


ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
  def __init__(self, dbname):
    pass

  def __del__(self):
    pass

  def dbcommit(self):
    pass

  def getentryid(self, table, field, value, createnew=True):
    """Returns an entry id and creates it if it is not present."""
    return None

  def addtoindex(self, url, soup):
    """Indexes a given page."""
    print 'Indexing', url

  def gettextonly(self, soup):
    """Extracts all text from a html page, i.e. strips the tags."""
    return None

  def separatewords(self, text):
    """Splits words by non-whitespace characters."""
    return None

  def isindexed(self, url):
    return False

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
        except:
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
    pass
