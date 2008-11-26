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
    pass

  def createindextables(self):
    """Create the database tables."""
    pass
