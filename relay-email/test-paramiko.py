import paramiko, base64
import os
import sys
import time
import datetime

next_flush = time.time()
num_email_sent = 0
while True:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('ssh.phx.nearlyfreespeech.net', username='westpoint777_everydayrelay', password='ep1574213')

        stdin, stdout, stderr = ssh.exec_command('exec /home/public/env/bin/python2.7 /home/public/relay-email/quickstart.py')

        if stderr:
            for line in stderr:
                print '... ERROR:' + line.strip('\n')
        else:
            for line in stdout:
                if "Sending" in line.strip('\n'):
                    num_email_sent += 1
        ssh.close()

        time.sleep(1)
        if time.time() > next_flush:
            next_flush = time.time() + 3600
            curts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print "%s: Sent %s emails" % (curts, num_email_sent)
            num_email_sent = 0

    except Exception, msg:
        print "Error: test-paramiko.py ran into issues: %s" % msg
        time.sleep(1)
