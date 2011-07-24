import elementtree.ElementTree
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app, login_required
from google.appengine.api import users
import gdata.calendar.client
import gdata.calendar.data
import atom
import time

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        text = self.request.get("text")

        if text == "":
            self.response.out.write('[Error] Please pass <text> as argument')
            return

        client = gdata.calendar.client.CalendarClient(source='company-appname-v1')
        client.ClientLogin('sjkim.test@gmail.com', 'ahenahen', client.source)

        event = gdata.calendar.data.CalendarEventEntry()
        event.title = atom.data.Title(text=text)

        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 180))
        event.when.append(gdata.calendar.data.When(start=start_time))

        event.when[0].reminder.append(gdata.data.Reminder(minutes='1'))
        
        new_event = client.InsertEvent(event)

        self.response.out.write('SMS is sent\n')
        self.response.out.write(new_event.GetHtmlLink().href)


application = webapp.WSGIApplication([('/sendsms', MainPage)], debug=True);

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main();
