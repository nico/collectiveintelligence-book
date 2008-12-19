import time
import urllib2
import xml.dom.minidom

# For nicolasweber@gmx.de / kayak!
kayakkey = 'ESxXILZlrprRyXZPtPLxig'


def getkayaksession():
  url = 'http://www.kayak.com/k/ident/apisession?token=%s&version=1' % kayakkey
  doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
  sid = doc.getElementsByTagName('sid')[0].firstChild.data
  return sid


def flightsearch(sid, origin, destination, depart_date):

  url = 'http://www.kayak.com/s/apisearch?basicmode=true&oneway=y'
  url += '&origin=%s&destination=%s' % (origin, destination)
  url += '&depart_date=%s&return_date=none&depart_time=a' % depart_date
  url += '&return_time=a&travelers=1&cabin=e&action=doFlights&apimode=1'
  url += '&_sid_=%s&version=1' % sid
  print url

  doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
  taglist = doc.getElementsByTagName('searchid')
  if len(taglist) == 0:
    raise Exception(doc.toxml())

  searchid = taglist[0].firstChild.data
  return searchid


def flightsearchresults(sid, searchid):

  def parseprice(p):  # strip currency and commas
    return float(p[1:].replace(',', ''))

  # poll until search is done (XXX: really necessary?)
  while 1:
    time.sleep(2)

    url = 'http://www.kayak.com/s/basic/flight?'
    url += 'searchid=%s&c=5&apimode=1&_sid_=%s&version=1' % (searchid, sid)
    doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())

    morepending = doc.getElementsByTagName('morepending')[0].firstChild
    if morepending == None or morepending.data == 'false': break

  # Read all results
  url = 'http://www.kayak.com/s/basic/flight?'
  url += 'searchid=%s&c=999&apimode=1&_sid_=%s&version=1' % (searchid, sid)
  doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())

  prices = doc.getElementsByTagName('price')
  departures = doc.getElementsByTagName('depart')
  arrivals = doc.getElementsByTagName('arrive')
  assert len(prices) == len(departures) == len(arrivals)

  return zip([p.firstChild.data.split(' ')[1] for p in departures],
             [p.firstChild.data.split(' ')[1] for p in arrivals],
             [parseprice(p.firstChild.data) for p in prices])


def createschedule(people, dest, dep, ret):
  sid = getkayaksession()
  flights = {}

  for p in people:
    name, origin = p

    # outbound flight
    searchid = flightsearch(sid, origin, dest, dep)
    flights[(origin, dest)] = flightsearchresults(sid, searchid)

    # return flight
    searchid = flightsearch(sid, dest, origin, ret)
    flights[(origin, dest)] = flightsearchresults(sid, searchid)

  return flights


if __name__ == '__main__':
  import optimization
  f = createschedule([('Nico', 'SFO'), ('Kerstin', 'SFO')], 'LGA',
      dep='12/30/2008', ret='1/2/2009')

  domain = [(0, 30)] * len(f)
  s = optimization.geneticoptimize(domain, optimization.costfunc(f, 'LGA'))
  optimization.printschedule(s, 'LGA')
