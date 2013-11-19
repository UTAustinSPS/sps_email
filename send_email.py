# This script sends an HTML file in an email to specified recipients
# using information provided by user

__author__ = 'Evan Ott (evan.ott@utexas.edu)'


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import getopt
import os
import string
import re
import smtplib
import sys

GMAIL_SERVER = 'smtp.gmail.com:587'


def send_email(html_email, to, cc, bcc, senders_email, subject):
  # make sure we have input for everything
  if len(html_email) == 0:
    html_email = open(input('HTML file containing message: ')).read()
  if len(to) == 0:
    to = input('To (separated by spaces): ')
  if len(cc) == 0:
    cc = input('Cc (separated by spaces): ')
  if len(bcc) == 0:
    bcc = input('Bcc (separated by spaces): ')

  if len(senders_email) == 0:
    senders_email = input('Sender\'s Gmail Address: ')
  password = getpass.getpass()

  # sanitize input
  to = to.strip()
  to = to.replace(',','')
  to = to.replace(';','')
  cc = cc.strip()
  cc = cc.replace(',','')
  cc = cc.replace(';','')
  bcc = bcc.strip()
  bcc = bcc.replace(',','')
  bcc = bcc.replace(';','')
  senders_email = senders_email.strip()

  if len(subject) == 0:
    subject = input('Subject: ')
  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = senders_email
  msg['To'] = ", ".join(re.split('\s+',to))
  msg['Cc'] = ", ".join(re.split('\s+',cc))
  
  if input('info correct? y/n ') in ['y', 'Y']:
    part = MIMEText(html_email, 'html')
    msg.attach(part)

    try:
      server = smtplib.SMTP(GMAIL_SERVER)
      server.starttls()
      server.login(senders_email, password)
      if len(to) > 0:
        to = re.split('[,;]?\s+', to)
      else:
        to = []
      if len(cc) == 0 and len(bcc) == 0:
        server.sendmail(senders_email, to, msg.as_string())
      else:
        if len(cc) > 0:
          cc = re.split('[,;]?\s+', cc)
        else:
          cc = []
        if len(bcc) > 0:
          bcc = re.split('[,;]?\s+', bcc)
        else:
          bcc = []
        server.sendmail(senders_email, to + cc + bcc, msg.as_string())
      print('Email sent!')
    finally:
      server.quit()
  else:
    print('Email cancelled, please try again')

HELP_MESSAGE = '\nUsage: python send_email.py [opts]\n\
Send emails containing HTML\n\
Command with no options yields a shell where user can input all paramters\n\
Command with options will prompt user for password and unspecified information only\n\
\n\
OPTIONS\n\
-h\n\
\tDisplay this message\n\
-t ADDRESSES\n\
\tSet the "to" field of the email. ADDRESSES can be a single address or list\n\
\tof addresses in quotes, separated by spaces. For example, "cns@utexas.edu kopp@hep.utexas.edu".\n\
-c ADDRESSES\n\
\tSet the "cc" field of the email. See above for ADDRESSES formatting.\n\
-b ADDRESSES\n\
\tSet the "bcc" field of the email. See above for ADDRESSES formatting.\n\
-f EMAIL\n\
\tSet the sender\'s email address. Before sending, system will prompt user for password for\n\
\tthis account. Current version only supports gmail/utexas accounts.\n\
-s SUBJECT\n\
\tSet the subject of the email. If more than one word, will need to use double quotes.\n\
\t"This is an example subject".\n\
-i FILE\n\
\tSet the filename of the HTML document containing what should be sent.'
def main(argv):
  try:
    opts, args = getopt.getopt(argv,"ht:c:b:s:f:i:")
  except getopt.GetoptError:
    print(HELP_MESSAGE)
    sys.exit(2)
  html_email = ''
  to = ''
  cc = ''
  bcc = ''
  senders_email = ''
  subject = ''
  for opt, arg in opts:
    if opt == '-h':
      print(HELP_MESSAGE)
      sys.exit()
    elif opt in ('-t', '--to'):
      to = arg
    elif opt in ('-c', '--cc'):
      cc = arg
    elif opt in ('-b', '--bcc'):
      bcc = arg
    elif opt in ('-s', '--subject'):
      subject = arg
    elif opt in ('-f', '--from'):
      senders_email = arg
    elif opt in ('-i', '--input'):
      html_email = open(arg).read()
  try:
    send_email(html_email, to, cc, bcc, senders_email, subject)
  except smtplib.SMTPAuthenticationError as e:
    print(e[1])
    print('Sending failed.')
if __name__ == '__main__':
  main(sys.argv[1:])
