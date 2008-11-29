def serve_search(environ, start_response):
  start_response('200 OK',[('Content-type','text/html')])
  return ['<html><body>Hello World!</body></html>\n']

#from wsgiref.handlers import CGIHandler
#CGIHandler().run(application)

from wsgiref import simple_server
httpd = simple_server.WSGIServer(
    ('', 8000),
    simple_server.WSGIRequestHandler,
    )
httpd.set_app(serve_search)
httpd.serve_forever()
