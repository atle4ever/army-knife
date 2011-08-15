import urllib, urllib2
import md5
import json

mPasswd = '9fed0b251f717554a6d5c7e27dbba4b0'
appId = 'maildelivery'
appToken = 'api4e45dc2f22799'
userId = 'td4af1291294b0a'
sessionToken = 'td4e48c678f317b'

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

args = urllib.urlencode({'key' : key, 'fields': 'duedate,duetime'})
res = urllib2.urlopen(url='http://api.toodledo.com/2/tasks/get.php',
        data=args)
json_ = json.loads(res.read())

num = json_.pop(0)['total']

for j in json_:
    if j['completed'] == 0:
        print j['title']
        print j
