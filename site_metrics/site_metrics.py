import smtplib
import sqlite3
import time

db_name = '/home/public/django/db.sqlite3'
eg_name = '/home/public/email-generator/todo.db'

prev_users = set()

username = 'everydayrelay@gmail.com'
password = 'ep1574213'
def send_gmail(subject):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)

    to = ['eugenepark3@gmail.com', 'eugenep@netapp.com']
    header = 'To:' + ", ".join(to) + '\n' + 'From: ' + username + '\n' + 'Subject: ' + subject + '\n'
    msg = header + '\n' + subject + '\n\n'

    server.sendmail(username, to, msg)
    server.quit()

con = sqlite3.connect(db_name)
next_flush = time.time()
r_email = ''
rs_email = ''
while True:
    msg = ''

    con_next = sqlite3.connect(eg_name)
    with con_next:
        cur_next = con_next.cursor()
        cur_next.execute('SELECT cur_email from table_r')
        row = cur_next.fetchall()[0]
        tmp_r = str(row[0])
        msg += "cur email: %s (prev: %s)\n" % (tmp_r, r_email)
        if tmp_r != r_email:
            r_email = tmp_r

        cur_next.execute('SELECT cur_email from table_rs')
        row = cur_next.fetchall()[0]
        tmp_rs = str(row[0])
        msg += "cur email: %s (prev: %s)\n" % (tmp_rs, rs_email)
        if tmp_rs != rs_email:
            rs_email = tmp_rs

    con = sqlite3.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute('SELECT username from auth_user')
        rows = cur.fetchall()
        cur_users = set([row[0] for row in rows])

    diff = cur_users.difference(prev_users)
    diff_msg = ""
    if diff > 0:
        prev_users = cur_users
        diff_msg += ', '.join(diff)
    msg += "%s new users! (cur users: %s)\n%s\n" % (len(diff), len(cur_users), diff_msg)


    send_gmail(msg)
    time.sleep(28800) # every 8 hours
