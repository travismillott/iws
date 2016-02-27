#!/usr/bin/env python

import cgi
import argparse
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

with open('index.html','r') as f:
  INDEX_HTML = f.read()


def parseArgs():
    parser = argparse.ArgumentParser(description='IWS Project Server')
    parser.add_argument('-p', '--port', default='80', type=int,
                        help="Port for incoming http connections")
    return parser.parse_args()



class FormPage(Resource):
    def render_GET(self, request):
        return INDEX_HTML

    def render_POST(self, request):
        return '<html><body>You submitted: %s</body></html>' % (cgi.escape(str(request.args)),)


if __name__ == "__main__":
  args = parseArgs()
  root = Resource()
  root.putChild("", FormPage())
  factory = Site(root)
  reactor.listenTCP(args.port, factory)
  reactor.run()

