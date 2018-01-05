#!/usr/bin/python2

import commands
import cgi

if commands.getstatusoutput("docker run -dit --name docker_shell nick:v3")[0] == 0:
	print "<form action='/docker_shell.html'>"

	print "</form>"
else:
	print "hello "
