#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from requests import get
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from email.Utils import parseaddr, formataddr

### CONFIG
# list of urls that will be checkek for 200 status and text
sites = {
    'http://en.wikipedia.org/wiki/Hacker_News' : u'Initially it was called Startup News or occasionally News.YC',
    'http://www.washingtonpost.com/' : u'Politics',
    'http://www.rackspace.com/' : u'Managed Hosting',
}

mail_config = {
    'host' : 'smtp.gmail.com',
    'port' : 587,
    'username' : 'youremail@gmail.com',
    'password' : 'yourpass',
    'to' : 'youremail@gmail.com',
    'mail_from' : 'youremail@gmail.com',
}
### END OF CONFIG. 
    
class ServerError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

def send_email(sender, recipient, subject, body, host='localhost', port='25', username=None, password=None, header_charset='UTF-8'):
 
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            body.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break

    sender_name, sender_addr = parseaddr(sender)
    recipient_name, recipient_addr = parseaddr(recipient)

    sender_name = str(Header(unicode(sender_name), header_charset))
    recipient_name = str(Header(unicode(recipient_name), header_charset))

    sender_addr = sender_addr.encode('ascii')
    recipient_addr = recipient_addr.encode('ascii')

    msg = MIMEText(body.encode(body_charset), 'plain', body_charset)
    msg['From'] = formataddr((sender_name, sender_addr))
    msg['To'] = formataddr((recipient_name, recipient_addr))
    msg['Subject'] = Header(unicode(subject), header_charset)

    smtp = SMTP('{host}:{port}'.format(host=host, port=port))
    smtp.starttls()
    if username and password:
        smtp.login(username,password)
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.quit()
    
def url_ok(url, search_for):
    r = get(url)
    if r.status_code != 200:
        error = u"{url} returns unexpected code {code}".format(url=url, code=r.status_code)
        raise ServerError(error)
    elif search_for not in r.text:
        error = u"{url} returns code 200 OK, but text '{text}' not found".format(url=url,text=search_for)
        raise ServerError(error)
    return True
    
def main():
    global sites
    global mail_config
    for url, search_for in sites.iteritems():
        try:
            url_ok(url,search_for)
        except ServerError as error:
            subject = u'error {url} {time}'.format(url=unicode(url),
                                                  time=unicode(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")))
            print "error mail sent"
            
            send_email(mail_config['mail_from'],
                      mail_config['to'] ,
                      subject,
                      unicode(error),
                      mail_config['host'],
                      mail_config['port'],
                      mail_config['username'],
                      mail_config['password'])

if __name__ == "__main__":
    main()
