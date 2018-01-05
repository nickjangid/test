#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
 

i = cgi.FormContent()['n1'][0]


if i == 'namenode':
	print "location: ../namenode.html"
	print


		
#	commands.getoutput("ansible-plabook /finalpart1/namenode.yml")

elif i == 'datanode':
#	commands.getoutput("ansible-plabook /finalpart1/datanode.yml")
	print "location: ../datanode.html"
	print


elif i == 'job':
	print "location: ../jobtracker.html"
	print
elif i == 'task':
	print "location: ../tasktracker.html"
	print

else:
	print "error"



