import urllib, urllib2
import md5
import json
from datetime import datetime, timedelta 

from toodledo_util import strOfDate

mPasswd = '9fed0b251f717554a6d5c7e27dbba4b0'
appId = 'maildelivery'
appToken = 'api4e45dc2f22799'
userId = 'td4af1291294b0a'
sessionToken = 'td4e4e6e19c3c9a'

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
#m = md5.new()
#m.update(userId)
#m.update(appToken)
#sig = m.hexdigest()
#args = urllib.urlencode({'userid' : userId, 'appid' : appId, 'sig' : sig})
#res = urllib2.urlopen(url='http://api.toodledo.com/2/account/token.php',
#        data=args)
#
#json_ = json.loads(res.read())
#sessionToken = json_['token']
#print sessionToken

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

        if duedate in taskMap:
            taskMap[duedate].append(title)
        else:
            taskMap[duedate] = [title]


taskList = taskMap.items()
taskList.sort()

for due, tasks in taskList :
    print due
    for t in tasks :
        print t
