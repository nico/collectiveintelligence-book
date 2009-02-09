import urllib2
import xml.dom.minidom

zwskey = 'X1-ZWz1chwxis15aj_9skq6'

def getaddressdata(address, city):
  escad = address.replace(' ', '+')

  url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
  url += 'zws-id=%s&address=%s&citystatezip=%s' % (zwskey, escad, city)

  #print url
  doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
  code = doc.getElementsByTagName('code')[0].firstChild.data

  #print doc.toxml()
  if code != '0': return None

  # Success!
  try:
    zipcode = doc.getElementsByTagName('zipcode')[0].firstChild.data
    use = doc.getElementsByTagName('useCode')[0].firstChild.data
    year = doc.getElementsByTagName('yearBuilt')[0].firstChild.data
    bath = doc.getElementsByTagName('bathrooms')[0].firstChild.data
    bed = doc.getElementsByTagName('bedrooms')[0].firstChild.data
    #rooms = doc.getElementsByTagName('totalRooms')[0].firstChild.data
    price = doc.getElementsByTagName('amount')[0].firstChild.data
  except Exception, e:
    #print e
    return None

  #return zipcode, use, int(year), float(bath), int(bed), int(rooms), price
  return zipcode, use, int(year), float(bath), int(bed), price


def getpricelist():
  return filter(None, [getaddressdata(line.strip(), 'Cambridge,MA')
      for line in open('addresslist.txt')])


if __name__ == '__main__':
  import drawtree
  import treepredict

  housedata = getpricelist()
  print housedata
  tree = treepredict.buildtree(housedata, scorefun=treepredict.variance)
  drawtree.drawtree(tree, 'zillow.png')
  print "Wrote zillow.png"
