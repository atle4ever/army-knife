from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        to = self.request.get("to");
        subject = self.request.get("subject");
        body = self.request.get("body");

        self.response.headers['Content-Type'] = 'text/plain'

        if to == "" or subject == "" or body == "" :
            self.response.out.write('[Error] Please pass <to>, <subject>, <body> as arguments')
            return

        mail.send_mail(sender="atle4ever@gmail.com", to=to, subject=subject, body=body);
        self.response.out.write('Mail is sent')


application = webapp.WSGIApplication([('/sendmail', MainPage)], debug=True);

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main();
