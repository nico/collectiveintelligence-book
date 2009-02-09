import urllib2
import xml.dom.minidom

apikey = '479NUNJHETN'

def getrandomratings(c):
  url = 'http://services.hotornot.com/rest/?app_key=%s' % apikey
  url += '&method=Rate.getRandomProfile&retrieve_num=%d' % c
  url += '&get_rate_info=true&meet_users_only=true'

  doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())

  emids = doc.getElementsByTagName('emid')
  ratings = doc.getElementsByTagName('rating')

  result = []
  for e, r in zip(emids, ratings):
    if r.firstChild != None:
      result.append( (e.firstChild.data, r.firstChild.data) )
  return result


stateregions={'New England':['ct','mn','ma','nh','ri','vt'],
             'Mid Atlantic':['de','md','nj','ny','pa'],
             'South':['al','ak','fl','ga','ky','la','ms','mo',
                      'nc','sc','tn','va','wv'],
             'Midwest':['il','in','ia','ks','mi','ne','nd','oh','sd','wi'],
             'West':['ak','ca','co','hi','id','mt','nv','or','ut','wa','wy']}


def getpeopledata(ratings):
  result = []
  for emid, rating in ratings:
    url = 'http://services.hotornot.com/rest/?app_key=%s' % apikey
    url += '&method=MeetMe.getProfile&emid=%s&get_keywords=true' % emid

    try:
      rating = int(float(rating) + 0.5)
      doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
      #print doc.toxml()
      gender = doc.getElementsByTagName('gender')[0].firstChild.data
      age = doc.getElementsByTagName('age')[0].firstChild.data
      loc = doc.getElementsByTagName('location')[0].firstChild.data

      region = None
      for r, s in stateregions.iteritems():
        if loc[0:2] in s: region = r

      if region:
        result.append( (gender, int(age), region, rating) )
    except:
      pass
  return result


if __name__ == '__main__':
  d = getrandomratings(50)

  # hu, all results are always of the same gender?
  pdata = getpeopledata(d)
  print pdata

  import drawtree
  import treepredict

  tree = treepredict.buildtree(pdata, treepredict.variance)
  treepredict.prune(tree, 0.5)
  drawtree.drawtree(tree, 'hottree.png')
  print 'Wrote hottree.png'
