from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from sendmail_util import sendmail

class MainPage(webapp.RequestHandler):
    def get(self):
        to = self.request.get("to");
        subject = self.request.get("subject");
        body = self.request.get("body");
        html= self.request.get("html");

        self.response.headers['Content-Type'] = 'text/plain'

        if to == "" or subject == "" or (body == "" and html == ""):
            self.response.out.write('[Error] Please pass <to>, <subject>, [<body>|<html>] as arguments')
            return

        sendmail(to, subject, body, html)

        self.response.out.write('Mail is sent')


application = webapp.WSGIApplication([('/sendmail', MainPage)], debug=True);

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main();
