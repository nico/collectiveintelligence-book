from math import tanh
import sqlite3 as sqlite  # use the bundled mysq   l

class searchnet:
  def __init__(self, dbname):
    self.con = sqlite.connect(dbname)

  def __del__(self):
    self.con.close()

  def maketables(self):
    self.con.execute('create table hiddennode(create_key)')
    self.con.execute('create table wordhidden(fromid, toid, strength)')
    self.con.execute('create table hiddenurl(fromid, toid, strength)')
    self.con.commit()

  def tablename(self, layer):
    return ['wordhidden', 'hiddenurl'][layer]

  def getstrength(self, fromid, toid, layer):
    """Gets a connection strength from the db, returns a default value if
    no value is found in the db."""
    table = self.tablename(layer)
    res = self.con.execute(
        'select strength from %s where fromid = %d and toid = %d'
        % (table, fromid, toid)).fetchone()
    if res == None:
      return [-0.2, 0][layer]
    return res[0]

  def setstrength(self, fromid, toid, layer, strength):
    table = self.tablename(layer)
    res = self.con.execute(
        'select rowid from %s where fromid = %s and toid = %s'
        % (table, fromid, toid)).fetchone()
    if res == None:
      self.con.execute('insert into %s (fromid, toid, strength) ' % table
          + 'values (%d, %d, %f)' % (fromid, toid, strength))
    else:
      self.con.execute('update %s set strength %s where rowid = %d'
          % (table, strength, res[0]))

  def generatehiddennode(self, wordids, urls):
    """Checks if a given combination of words was already learned. If not,
    connects the words to a new hidden node and this hidden node to urls.
    
    This means that the set of urls for a given set of words can not be
    changed once it has been set."""
    if len(wordids) > 3: return None

    # Did we already create a node for this set of words?
    createkey = '_'.join(sorted(map(str, wordids)))
    res = self.con.execute(
        'select rowid from hiddennode where create_key = "%s"'
        % createkey).fetchone()

    # If not, do so now
    if res == None:
      cur = self.con.execute('insert into hiddennode (create_key) values ("%s")'
          % createkey)
      hiddenid = cur.lastrowid

      # create default values that indicate the connection between wordids and
      # urls
      for wordid in wordids:
        self.setstrength(wordid, hiddenid, 0, 1.0/len(wordids))
      for urlid in urls:
        self.setstrength(hiddenid, urlid, 1, 0.1)
      self.con.commit()

  def getallhiddenids(self, wordids, urlids):
    """Returns all hidden nodes connected to either wordids or urlids."""
    l1 = set()
    for wordid in wordids:
      cur = self.con.execute(
          'select toid from wordhidden where fromid = %d' % wordid)
      for row in cur: l1.add(row[0])
    for urlid in urlids:
      cur = self.con.execute(
          'select fromid from hiddenurl where toid = %d' % urlid)
      for row in cur: l1.add(row[0])
    return list(l1)

  def setupnetwork(self, wordids, urlids):
    # XXX: it's weird that this assigns to member variables
    # value lists
    self.wordids = wordids
    self.hiddenids = self.getallhiddenids(wordids, urlids)
    self.urlids = urlids

    # node outputs
    self.ai = [1.0] * len(self.wordids)
    self.ah = [1.0] * len(self.hiddenids)
    self.ao = [1.0] * len(self.urlids)

    # create weight matrix
    self.wi = [[self.getstrength(wordid, hiddenid, 0)
      for hiddenid in self.hiddenids]
      for wordid in wordids]
    self.wo = [[self.getstrength(hiddenid, urlid, 1)
      for urlid in self.urlids]
      for hiddenid in self.hiddenids]

  def feedforward(self):
    for i in range(len(self.wordids)):
      self.ai[i] = 1.0

    for j in range(len(self.hiddenids)):
      sum = 0.0
      for i in range(len(self.wordids)):
        sum += self.ai[i] * self.wi[i][j]
      self.ah[j] = tanh(sum)

    for k in range(len(self.urlids)):
      sum = 0.0
      for j in range(len(self.hiddenids)):
        sum += self.ah[j] * self.wo[j][k]
      self.ao[k] = tanh(sum)

    return self.ao[:]

  def getresult(self, wordids, urlids):
    self.setupnetwork(wordids, urlids)
    return self.feedforward()


if __name__ == '__main__':
  net = searchnet('nn.db')
  net.maketables()

  words = [101, 102]
  urls = [201, 202, 203]
  net.generatehiddennode(words, urls)

  for c in net.con.execute('select * from hiddennode'): print c
  for c in net.con.execute('select * from wordhidden'): print c
  for c in net.con.execute('select * from hiddenurl'): print c
  print net.getallhiddenids([101], [202, 203])

  print net.getresult([101], [201, 203])
