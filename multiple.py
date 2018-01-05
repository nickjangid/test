#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print


size = cgi.FormContent()['size'][0]
n1 = cgi.FormContent()['n1'][0]

if n1 == 'hdfs':
	print "<form action='hdfs.py'"
	for i in range(int(size)+1):
		print "ip{0}:<input type='text' name='ip{0}' /><br />".format(i)
	
	print "lv size in GB<input type='text' name='lv' /><br />"	
	print "<input type='submit' />"
	
	print "</form>"

elif n1 == 'mapred':
	print "<form action='mapred.py'"
	for i in range(int(size)+1):
		print "ip{0}:<input type='text' name='ip{0}' /><br />".format(i)
	print "<input type='text' name='n_ip' value='nameIP' />"
	print "<input type='submit' />"
	
	print "</form>"

else:
	print "you are out of way"
