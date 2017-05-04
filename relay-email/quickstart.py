import httplib2
import os
import re
import redis
import sys
import time

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import base64
import email
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes

import smtplib

from apiclient import errors


sys.path.append('/home/public/email-generator')
import EmailGenerator as ge

pool = redis.ConnectionPool(host='10.2.48.99', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
#SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
#APPLICATION_NAME = 'Gmail API Python Quickstart'
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = '/home/public/relay-email/client_secret.json'
APPLICATION_NAME = 'relayer'

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'relayer-2-21-16.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print "new credential"
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.
  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()
    #print 'Message snippet: %s' % message['snippet']
    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    mime_msg = email.message_from_string(msg_str)
    return_str = ''
    for part in mime_msg.walk():
        if part.get_content_type() == 'text/plain':
            return_str += part.get_payload()
    return return_str
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.
  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.b64encode(message.as_string())}

def SendMessage(service, user_id, message):
  """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    #return message
    return True
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return False

def DeleteMessage(service, user_id, msg_id):
  """Delete a Message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message to delete.
  """
  try:
    service.users().messages().delete(userId=user_id, id=msg_id).execute()
    print 'Message with id: %s deleted successfully.' % msg_id
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def send_email(me='', to=[], cc=[], bcc=[], subject='', message=''):
    try:
        me = me
        all = to+cc+bcc
        msg = email.mime.text.MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = me
        if to:
            msg['To'] = ', '.join(to)
        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)

        s = smtplib.SMTP('mail', 587)
        s.sendmail(me, all, msg.as_string())
        s.close()
        return True
    except Exception, err:
        print "cant send email %s" % err
        return False

################START################################
def main():
    """Shows basic usage of the Gmail API.
    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    print "starting main()"
    # 1. INIT
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # 2. Get <unread> emails, SENT, INBOX
    #results = service.users().messages().list(userId='me', labelIds='UNREAD').execute()
    results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results.get('messages', [])

    #'labelIDs', SENT, UNREAD 
    # TODO: only get UNREAD EMAILS
    for msg in messages:
        print "\n================================================="
        # 2A: get 'from', 'to', and 'snippet'  from the email
        id = msg['id']
        msgobj = GetMessage(service, 'me', id)
        body = GetMimeMessage(service, 'me', id)
        lblid = msgobj['labelIds']

        # REMOVE REPLIES PART OF MESSAGE
        lines = body.split('\n')
        last_reply_linenum = None
        if len(lines) > 1:
            if '>' in lines[-2]:
                found_x = False 
                last_reply_linenum = None
                for i, line in enumerate(reversed(lines)):
                    if found_x == False and '>' in line:
                        found_x = True
                    elif found_x == True and '>' not in line:
                        last_reply_linenum = i
                        break

                if last_reply_linenum:
                    last_reply_linenum += 3
        if last_reply_linenum:
            last_reply_linenum = len(lines) - last_reply_linenum
            lines = lines[:last_reply_linenum]
        body = '\n'.join(lines)
        print body
        # END REMOVE REPLIES OF MESSAGE
            
        to_email = ''
        from_email = ''
        subject = ''
        try:
            # headers is a list of dicts
            for kdict in msgobj['payload']['headers']:
                if kdict['name'] == 'Subject':
                    subject = kdict['value']   
                    print 'Subject: %s' % subject
                elif kdict['name'] == 'From':
                    possible_from = re.findall('\<\S+@\S+\>', kdict['value'])
                    if len(possible_from) > 0:
                        from_email = possible_from[0][1:-1]
                elif kdict['name'] == 'Received':
                    if not to_email:
                        if 'forward.nearlyfreespeech.net' in kdict['value']:
                            possible_to = re.findall('\<\S+@\S+\>', kdict['value'])
                            if len(possible_to) > 0:
                                to_email = possible_to[0][1:-1]
        except Exception, msg:
            print msg

        if not to_email or not from_email:
            print "cant parse from/to emails... deleting"
            DeleteMessage(service, 'me', id)
            continue

        # Lets see if we have enough credits
        username = r.hget('uemap', to_email)
        user_cre = r.hget('ucredits', username)
        try:
            if int(user_cre) < 1:
                print "sorry no credits so going to delete the email"
                DeleteMessage(service, 'me', id)
        except Exception, msg:
            print "error getting credit for %s (%s credits)\n%s" %  (username, user_cre, msg)

        success = False
        # at this point, we have (os), (r)/(rs), subject, body  
        from_redis_hashname = "fromkeys"
        if to_email.startswith('z'):
            print "This is type (r): %s" % to_email
            # 1. Get (e) from (r):(e) mapping of 'r' in redis
            my_e = r.hget('r', to_email)
            if my_e is not None:
                print "(e) for (r) %s is %s" % (to_email, my_e)
            else:
                print "unknown match (e) for (r) %s" % to_email
                continue

            # 2. Get (rs); create (rs) if first time seeing (os)->(r)
            from_key = "%s:%s" % (from_email, to_email)
            rs = r.hget(from_redis_hashname, from_key)
            if rs is None: # first time seeing it!
                print "RS doesnt exists creating a new one..."
                rs = ge.get_rs()
                print "New rs is %s" % rs

                # in redis, populated fromkeys 
                r.hset(from_redis_hashname, from_key, rs)
                # in reds, populate rs
                r.hset('rs', rs, from_key) 
                # save this email to username
                r.hset('uemap', rs, username)
            
            print "Sending email %s->%s" % (rs, my_e)
            msg_to_send = CreateMessage(rs, my_e, 'r', 'hi')

            success = send_email(me=rs, to=[my_e], subject=subject, message=body)
            username = r.hget('uemap', to_email)
            r.hincrby('ucredits', username, -1)

        elif to_email.startswith('y'):
            print "This is type (rs): %s" % to_email
            my_os_r = r.hget('rs', to_email)
            if my_os_r is None:
                print "unknown match (rs) %s" % to_email
                continue

            # send email(from=my_r, to=my_os) 
            my_os, my_r = my_os_r.split(':')
            print "Sending email %s->%s" % (my_r, my_os)
            msg_to_send = CreateMessage(my_r, my_os, 'rs', 'hi')

            success = send_email(me=my_r, to=[my_os], subject=subject, message=body)
            username = r.hget('uemap', to_email)
            r.hincrby('ucredits', username, -1)

        else:
            print "unknown type: %s" % to_email 

        #break
        # TODO: this works but need to not delete for now so i can test
        if success:
            DeleteMessage(service, 'me', id)

if __name__ == '__main__':
    main()
