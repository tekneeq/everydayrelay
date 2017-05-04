import argparse
import sqlite3
import datetime
import os

# email for (r) should start with 'z'
# email for (rs) should start with 'y'
#parser = argparse.ArgumentParser(description='generate emails')
#parser.add_argument('--r', action='store_true')
#parser.add_argument('--rs', action='store_true')

#args = parser.parse_args()

def increment(ele):
    str_part = ele[:4]
    int_part = ele[4:]

    tmp_int = 0
    if int(int_part) < 9999:
        # keep str and increment int
        tmp_int = int(int_part) + 1
        # if length is 4 then its good but if its less than 4 then we need to add 0's to the front
        if len(str(tmp_int)) < 4:
            to_add = 4 - len(str(tmp_int))
            zeros = ''
            for i in range(to_add):
                zeros += '0'

            int_part = zeros + str(tmp_int)    
        else:
            int_part = str(tmp_int)
    else:
        # increment str and add '0000'
        int_part = '0000'
        to_copy = list(reversed(list(str_part)))
        to_arr = reversed(list(str_part))

        # 'a' 97
        # 'z' 122
        raised = False
        for index, value in enumerate(to_arr):
            if index == 0:
                if ord(value) == 122:
                    to_copy[index] = 'a'
                    raised = True
                else:
                    to_copy[index] = chr(ord(value)+1)
                    raised = False
            else:
                if raised:
                    if ord(value) == 122:
                        to_copy[index] = 'a'
                        raised = True
                    else:
                        to_copy[index] = chr(ord(value)+1)
                        raised = False
                else:
                    break
        str_part = "".join(reversed(to_copy))
                    

    return str_part + int_part

#aaaa0000 => aaaa0001
#aaaa9999 => aaab0000
#aaaz9999 => aaba0000
#aazz9999 => abaa0000
#t1 = 'aaaa0000'
#t2 = 'aaaa9999'
#t3 = 'aaaz9999'
#t4 = 'aazz9999'
#ts = [t1, t2, t3, t4]
#for t in ts:
#    print "%s => %s" % (t, increment(t))

db_filename = '/home/public/email-generator/todo.db'
schema_filename = 'todo_schema.sql'
db_is_new = not os.path.exists(db_filename)

def get_r():
    with sqlite3.connect(db_filename) as conn:
        if db_is_new:
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

            conn.execute('insert into table_r (cur_email, insert_date) values (?, ?)', ('zaaaa0000@everydayrelay.com', datetime.datetime.now()))
            conn.execute('insert into table_rs (cur_email, insert_date) values (?, ?)', ('yaaaa0000@everydayrelay.com', datetime.datetime.now()))
        else:
            postfix = '@everydayrelay.com'
            new_email = ''
            tmp_email = ''

            new_email += 'z'
            cursor = conn.execute("SELECT cur_email from table_r")
            for row in cursor:
                tmp_email = row[0]

            splitted = tmp_email.split('@')[0]
            splitted = splitted[1:]
            incd = increment(splitted)
            new_email += incd
            new_email += postfix
        
            conn.execute("""update table_r set cur_email = ? where id=?""", (new_email, 1))

            return new_email

def get_rs():
    with sqlite3.connect(db_filename) as conn:
        if db_is_new:
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

            conn.execute('insert into table_r (cur_email, insert_date) values (?, ?)', ('zaaaa0000@everydayrelay.com', datetime.datetime.now()))
            conn.execute('insert into table_rs (cur_email, insert_date) values (?, ?)', ('yaaaa0000@everydayrelay.com', datetime.datetime.now()))
        else:
            postfix = '@everydayrelay.com'
            new_email = ''
            tmp_email = ''

            new_email += 'y'
            cursor = conn.execute("SELECT cur_email from table_rs")
            for row in cursor:
                tmp_email = row[0]

            splitted = tmp_email.split('@')[0]
            splitted = splitted[1:]
            incd = increment(splitted)
            new_email += incd
            new_email += postfix
        
            conn.execute("""update table_rs set cur_email = ? where id=?""", (new_email, 1))

            return new_email

#if args.r:
#    print get_r()
#elif args.rs:
#    print get_rs()
