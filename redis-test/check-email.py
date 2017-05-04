#import subprocess

#email_gen_script = '/home/public/email-generator/generate-email.py'

#cmd_r = [email_gen_script, '--r']
#cmd_rs = [email_gen_script, '--rs']

#p = subprocess.Popen(cmd_r, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#stdout, stderr = p.communicate()
#print stdout

#p = subprocess.Popen(cmd_rs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#stdout, stderr = p.communicate()
#print stdout

import sys

sys.path.append('/home/public/email-generator')
import EmailGenerator as ge


print "NEXT GENERATED EMAILS ARE:"
print ge.get_r()
print ge.get_rs()
