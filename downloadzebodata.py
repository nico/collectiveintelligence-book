from BeautifulSoup import BeautifulSoup

import collections
import re
import urllib2

chare = re.compile(r'[!-\.&]')
itemowners = collections.defaultdict(dict)

dropwords = [
    'a', 'new', 'some', 'more', 'my', 'own', 'the', 'many', 'other', 'another']

# XXX: Doesn't seem to work atm, because zebo's search is broken

currentuser = 0
for i in range(1, 51):
  c = urllib2.urlopen('http://member.zebo.com/Main?' +
      'event_key=USERSEARCH&wiowiw=wiw&keyword=car&page=%d' % i)
  soup = BeautifulSoup(c.read())
  for td in soup('td'):
    if 'class' in dict(td.attrs) and td['class'] == 'bgverdanasmall':
      items = [
          re.sub(chare, '', a.contents[0].lower()).strip() for a in td('a')]
      for item in items:
        # remove extra words
        txt = ' '.join([t for t in item.split(' ') if t not in dropwords])
        if len(txt) < 2: continue
        itemowners[txt][currentuser] = 1
      currentuser += 1

out = open('zebo.txt', 'w')
out.write('Item')
for user in range(0, currentuser): out.write('\tU%d' % user)
out.write('\n')
for item, owners in itemowners.iteritems():
  if len(owners) > 10:
    out.write(item)
    for user in range(0, currentuser):
      if user in owners: out.write('\t1')
      else: out.write('\t0')
    out.write('\n')
