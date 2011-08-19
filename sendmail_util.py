from google.appengine.api import mail

def sendmail(to, subject, body, html) :
    message = mail.EmailMessage(sender='atle4ever@gmail.com', subject=subject)
    message.to = to
    message.body = body
    message.html = html
    message.send()
