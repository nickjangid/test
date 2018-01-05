#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print

n1 = cgi.FormContent()['n1'][0]
size = cgi.FormContent()['size'][0]


if n1 == 'hdfs':
	print "<form action=hdfs2.py />"
	for i in range(int(size)):
		print "Enter your IP{0}<input type='text' name='ip{0}' />".format(i)
		print "<br />"
	print "enter data node disk size<input type='text' name='d_size' />"
	print "<input type='submit' />"
	print "</form>"

elif n1 == 'mr2':
	print "<form action=mapred2.py />"
	for i in range(int(size)):
		print "Enter your IP{0}<input type='text' name='ip{0}' />".format(i)
		print "<br />"
	print "enter namnnode IP<input type='text' name='n_ip' />"
	print "<input type='submit' />"
	print "</form>"

else:
	print "check again"


