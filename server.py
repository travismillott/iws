#!/usr/bin/env python

import cgi
import argparse
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.util import redirectTo


import utils

with open('index.html','r') as f:
  INDEX_HTML = f.read()

with open('feature_request.html','r') as f:
  FORM_HTML = f.read()


def parseArgs():
    parser = argparse.ArgumentParser(description='IWS Project Server')
    parser.add_argument('-p', '--port', default='80', type=int,
                        help="Port for incoming http connections")
    return parser.parse_args()



def showFeatureRequestTable():
  return INDEX_HTML.format(body=utils.createFeatureRequestTable())


class FeatureOverview(Resource):
    def render_GET(self, request):
        return showFeatureRequestTable()


class FormPage(Resource):
    def render_GET(self, request):
        return INDEX_HTML.format(body=FORM_HTML.format(validationMsg=''))

    def render_POST(self, request):
        validDict = utils.validateRequiredColumns(request.args)
        if utils.allArgsValid(validDict):
          utils.insertFeatureRequest(request.args)
          return redirectTo("/", request)

        return INDEX_HTML.format(body=FORM_HTML.format(validationMsg='<div style="color:red">Please fill in all fields</div>'))


if __name__ == "__main__":
  args = parseArgs()

  root = Resource()
  root.putChild("", FeatureOverview())
  root.putChild("new_feature", FormPage())
  factory = Site(root)
  reactor.listenTCP(args.port, factory)
  reactor.run()

