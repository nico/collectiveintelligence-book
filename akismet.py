#!/usr/bin/python

__version__ = "0.3"
__date__ = "2005-12-01"
__author__ = "David Lynch (kemayo AT Google's mail service DOT com)"
__copyright__ = "Copyright 2005, David Lynch"
__license__ = "New BSD"
__history__ = """
0.3 - 20051205 - Cleaned up __post.
0.2 - 20051201 - Added documentation, and tweaked the circumstances where an error
    will be thrown.
0.1 - 20051201 - Initial release.  Everything pretty much works.  Probably.
"""

import httplib
from urllib import urlencode

USERAGENT = ""
AKISMET_URL = "rest.akismet.com"
AKISMET_PORT = 80

class AkismetError(Exception):
    def __init__(self, response, statuscode):
        self.response = response
        self.statuscode = statuscode
    def __str__(self):
         return repr(self.value)

def __post(request, host, path, port = 80):
    connection = httplib.HTTPConnection(host, port)
    connection.request("POST", path, request,
        {"User-Agent":"%s | %s/%s" % (USERAGENT,"Akistmet.py", __version__),
        "Content-type":"application/x-www-form-urlencoded"})
    response = connection.getresponse()
    
    return response.read(), response.status

def verify_key(key, blog):
    """Find out whether a given WordPress.com API key is valid.
    Required parameters:
        key: A WordPress.com API key.
        blog: URL of the front page of the site comments will be submitted to.
    Returns True if a valid key, False if invalid.
    """
    response, status = __post("key=%s&blog=%s" % (key,blog), AKISMET_URL, "/1.1/verify-key", AKISMET_PORT)
    
    if response == "valid":
        return True
    elif response == "invalid":
        return False
    else:
        raise AkismetError(response, status)

def comment_check(key, blog, user_ip, user_agent, **other):
    """Submit a comment to find out whether Akismet thinks that it's spam.
    Required parameters:
        key: A valid WordPress.com API key, as tested with verify_key().
        blog: URL of the front page of the site the comment will appear on.
        user_ip: IP address of the being which submitted the comment.
        user_agent: User agent reported by said being.
    Suggested "other" keys: "permalink", "referrer", "comment_type", "comment_author",
    "comment_author_email", "comment_author_url", "comment_content", and any other HTTP
    headers sent from the client.
    More detail on what should be submitted is available at:
    http://akismet.com/development/api/
    
    Returns True if spam, False if ham.  Throws an AkismetError if the server says
    anything unexpected.
    """
    
    request = {'blog': blog, 'user_ip': user_ip, 'user_agent': user_agent}
    request.update(other)
    response, status = __post(urlencode(request), "%s.%s" % (key,AKISMET_URL), "/1.1/comment-check", AKISMET_PORT)
    
    if response == "true":
        return True
    elif response == "false":
        return False
    else:
        raise AkismetError(response, status)

def submit_spam(key, blog, user_ip, user_agent, **other):
    """Report a false negative to Akismet.
    Same arguments as comment_check.
    Doesn't return anything.  Throws an AkismetError if the server says anything.
    """
    request = {'blog': blog, 'user_ip': user_ip, 'user_agent': user_agent}
    request.update(other)
    response, status = __post(urlencode(request), "%s.%s" % (key,AKISMET_URL), "/1.1/submit-spam", AKISMET_PORT)
    if status != 200 or response != "":
        raise AkismetError(response, status)

def submit_ham(key, blog, user_ip, user_agent, **other):
    """Report a false positive to Akismet.
    Same arguments as comment_check.
    Doesn't return anything.  Throws an AkismetError if the server says anything.
    """
    request = {'blog': blog, 'user_ip': user_ip, 'user_agent': user_agent}
    request.update(other)
    response, status = __post(urlencode(request), "%s.%s" % (key,AKISMET_URL), "/1.1/submit-ham", AKISMET_PORT)
    if status != 200 or response != "":
        raise AkismetError(response, status)
