#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


cName=cgi.FormContent()['x'][0]


cremovestatus=commands.getstatusoutput("sudo docker rm -f {0}".format(cName))

if cremovestatus[0]  == 0:
	print "location:  doc_manage.py"
	print
else:
	print "not removed"




