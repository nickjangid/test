#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print 

i = cgi.FormContent()['inp'][0]

print "<pre>"

print commands.getoutput("sudo docker exec web_server '{}'".format(i))

print "</pre>"


