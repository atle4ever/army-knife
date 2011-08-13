from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import httplib, urllib
import json

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        # Get session token
        httpConn= httplib.HTTPConnection("api.toodledo.com", 80)
        httpConn.connect()

        args = urllib.urlencode({'userid' : 'td4af1291294b0a', 'appid' : 'maildelivery', 'sig' : '7908c91935f48cc80635f168a8d7f592'})
        httpConn.request('POST', '/2/account/token.php', args)

        httpRes = httpConn.getresponse()
        if httpRes.status == httplib.OK:
            text = httpRes.read()
            json_ = json.loads(text)
            token = json_['token']

application = webapp.WSGIApplication([('/toodledo', MainPage)], debug=True);

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main();
