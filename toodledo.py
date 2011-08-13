from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db

import httplib, urllib
import json
from datetime import datetime, timedelta

class Token(db.Model):
    token = db.StringProperty()
    timeStamp = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        # Get session token
        tokens = db.GqlQuery("SELECT *"
                "FROM Token "
                "WHERE timeStamp < :1 "
                "ORDER BY timeStamp DESC LIMIT 1",
                datetime.now() + timedelta(hours=4))

        if tokens.count() == 0:
            httpConn= httplib.HTTPConnection("api.toodledo.com", 80)
            httpConn.connect()

            args = urllib.urlencode({'userid' : 'td4af1291294b0a', 'appid' : 'maildelivery', 'sig' : '7908c91935f48cc80635f168a8d7f592'})
            httpConn.request('POST', '/2/account/token.php', args)

            httpRes = httpConn.getresponse()
            if httpRes.status == httplib.OK:
                text = httpRes.read()
                json_ = json.loads(text)
                
                token = Token()
                token.token = json_['token']
                token.put()
        else:
            token = tokens[0]

        print token.token
        print token.timeStamp
        print datetime.now()

application = webapp.WSGIApplication([('/toodledo', MainPage)], debug=True);

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main();
