import cgi
import searchengine

template = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Next Google</title>
</head>
<body>
<form>
Search for: <input type="text" name="q" value="%(query_words)s">
<input type="submit" value="Search!">
</form>
%(results)s
</body>
</html>
"""

def serve_search(environ, start_response):

  query_words = ''
  results = ''
  if 'QUERY_STRING' in environ:
    query_dict = cgi.parse_qs(environ['QUERY_STRING'])
    if 'q' in query_dict:
      # parse_qs returns a list for values as query parameters can appear
      # several times (e.g. 'q=ddsview&q=makeicns'). Ignore all but the first
      # occurence of q.
      query_words = query_dict['q'][0]
      s = searchengine.searcher('searchindex.db')
      results = '<br>\n'.join(['%f: <a href="%s">%s</a>' % (score, url, url)
        for score, url in s.query(query_words)])
      results = results.encode('utf-8')

  # Note: this also returns html for favicon queries.
  start_response('200 OK',[('Content-type','text/html')])
  return [template % locals()]


if __name__ == '__main__':
  from wsgiref import simple_server
  httpd = simple_server.make_server('', 8000, serve_search)
  httpd.serve_forever()
