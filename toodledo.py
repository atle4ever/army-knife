from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os
import urllib, urllib2
import md5
import json
import logging
from datetime import datetime, timedelta

from toodledo_util import strOfDate

mPasswd = '9fed0b251f717554a6d5c7e27dbba4b0'
appId = 'maildelivery'
appToken = 'api4e45dc2f22799'
userId = 'td4af1291294b0a'
sessionToken = 'td4e4e6e19c3c9a'

class Session(db.Model):
    token = db.StringProperty()
    timeStamp = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # Get user id
        #m = md5.new()
        #m.update(email)
        #m.update(appToken)
        #sig = m.hexdigest()
        #args = urllib.urlencode({'appid' : appId, 'email' : email, 'pass' : passwd, 'sig' : sig})
        #res = urllib2.urlopen(url='http://api.toodledo.com/2/account/lookup.php', 
        #        data=args)
        #
        #json_ = json.loads(res.read())
        #userId = json_['userid']

        # Get session token
        session = db.GqlQuery("SELECT *"
                "FROM Session "
                "WHERE timeStamp > :1 "
                "ORDER BY timeStamp DESC LIMIT 1",
                datetime.now() - timedelta(hours=4))

        if session.count() == 0:
            m = md5.new()
            m.update(userId)
            m.update(appToken)
            sig = m.hexdigest()
            args = urllib.urlencode({'userid' : userId, 'appid' : appId, 'sig' : sig})
            res = urllib2.urlopen(url='http://api.toodledo.com/2/account/token.php',
                    data=args)

            json_ = json.loads(res.read())
            sessionToken = json_['token']

            session = Session()
            session.token = sessionToken
            session.put()
            logging.info("Get new token - Token: " + session.token + " TS: " + str(session.timeStamp))

        else:
            sessionToken = session[0].token
            logging.info("Retrieve stored token - Token: " + session[0].token + " TS: " + str(session[0].timeStamp))

        # Generating key
        m = md5.new()
        m.update(mPasswd)
        m.update(appToken)
        m.update(sessionToken)
        key = m.hexdigest()
        
        # Get tasks
        args = urllib.urlencode({'key' : key, 'fields': 'startdate,duedate'})
        res = urllib2.urlopen(url='http://api.toodledo.com/2/tasks/get.php',
                data=args)
        json_ = json.loads(res.read())
        
        num = json_.pop(0)['total']
        
        # date
        dueBoundary = datetime.now() + timedelta(days=7)
        dueBoundary = dueBoundary.strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        taskMap = {}
        
        for j in json_:
            if j['completed'] == 0:
                title = j['title']
                duedate = strOfDate(j['duedate'])
        
                if duedate > dueBoundary :
                    startdate = j['startdate']
                    if startdate == 0:
                        continue # due-date > today + 7 && no start-date
        
                    startdate = strOfDate(startdate)
                    if startdate > today :
                        continue # due-date > today + 7 && start-date > today

                    taskType = 'startdate'

                elif duedate == today :
                    taskType = 'today'

                elif duedate < today :
                    taskType = 'overdue'

                else :
                    taskType = 'normal'
                    
                if duedate in taskMap:
                    taskMap[duedate].append([title, taskType])
                else:
                    taskMap[duedate] = [[title, taskType]]
        
        taskList = taskMap.items()
        taskList.sort()

        template_values = { 'taskList' : taskList }
        path = os.path.join(os.path.dirname(__file__), 'toodledo_template.html')
        self.response.out.write(template.render(path, template_values))
        

application = webapp.WSGIApplication([('/toodledo', MainPage)], debug=True);

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main();
