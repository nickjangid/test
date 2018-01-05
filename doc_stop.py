#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


cName2=cgi.FormContent()['z'][0]


cstopstatus=commands.getstatusoutput("sudo docker stop {0}".format(cName2))

if cstopstatus[0]  == 0:
	print "location:  doc_manage.py"
	print
else:
	print "not stopped"




