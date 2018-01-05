#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


cName1=cgi.FormContent()['y'][0]


cstartstatus=commands.getstatusoutput("sudo docker start {0}".format(cName1))

if cstartstatus[0]  == 0:
	print "location:  doc_manage.py"
	print
else:
	print "not started"




