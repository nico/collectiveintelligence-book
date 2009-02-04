import akismet

defaultkey = '09d55c02ef86'
#pageurl = 'http://amnoid.de'
pageurl = 'http://groups.google.com'

#defaultagent = 'akismettest python script from the Collective Intelligence book'
defaultagent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; en-us) '
defaultagent += 'AppleWebKit/525.27.1 (KHTML, like Gecko) '
defaultagent += 'Version/3.2.1 Safari/525.27.1'


def isspam(comment, author, ip, agent=defaultagent, apikey=defaultkey):
  try:
    valid = akismet.verify_key(apikey, pageurl)
    if valid:
      return akismet.comment_check(apikey, pageurl, ip, agent,
          comment_content=comment, comment_author_email=author,
          comment_type='email')
    else:
      print 'Invalid key'
      return False
  except akismet.AkismetError, e:
    print e.response, e.statuscode
    return False


if __name__ == '__main__':
  print isspam('Buy Viagra!', 'rz223@hotmail.com', '127.0.0.1')
  print isspam("That's an interesting post. My vote goes to the green one",
      'jwz@gmail.com', '67.218.106.36')
