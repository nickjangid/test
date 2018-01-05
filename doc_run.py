#!/usr/bin/python2

import  doc_images



print "<h2>Launch your Container : </h2>"

print "<form action='doc_launch.py'>"

print "Select ur docker image :"
doc_images.docker_list()

print """
<br />
Enter ur container name: <input name='cname' />
<br />
<input type='submit' />
</form>
"""
