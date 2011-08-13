from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import httplib, urllib

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        # Get session token
        httpServ = httplib.HTTPConnection("api.toodledo.com", 80)
        httpServ.connect()

        params = urllib.urlencode({'userid' : 'td4af1291294b0a', 'appid' : 'maildelivery', 'sig' : '7908c91935f48cc80635f168a8d7f592'})
        httpServ.request('POST', '/2/account/token.php', params)

        response = httpServ.getresponse()
        if response.status == httplib.OK:
            print "Output from CGI request "
            lines = response.read().split('\n')
            for line in lines:
                print line.strip()


application = webapp.WSGIApplication([('/toodledo', MainPage)], debug=True);

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main();
