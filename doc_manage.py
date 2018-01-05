#!/usr/bin/python2


import commands

print "content-type: text/html"
print

print """
<script>
function lw(mycname)
{
//alert('hello');

document.location='doc_remove.py?x=' + mycname;

}
function lw1(mycname1)
{
//alert('hello');

document.location='doc_start.py?y=' + mycname1;

}
function lw2(mycname2)
{
//alert('hello');

document.location='doc_stop.py?z=' + mycname2;

}
</script>
"""


print "<table border='5'>"
print "<tr><th>Image Name</th><th>ContainerName</th><th>Status</th><th>Stop</th><th>Start</th><th>Remove</th></tr>"

z=1
for i in commands.getoutput("sudo docker ps -a").split('\n'):
	if z == 1:
		z+=1
		pass
	else:
		j=i.split()
		cStatus=commands.getoutput("sudo docker inspect {0} | jq '.[].State.Status'".format(j[-1]))

		print "<tr><td>" + j[1] + "</td><td>" + j[-1] + "</td><td>" + cStatus +  "</td><td><input value='" + j[-1]    +  "' type='button' onclick=lw2(this.value)  /></td><td> <input value='" + j[-1]    +  "' type='button' onclick=lw1(this.value)  /></td><td>  <input value='" + j[-1]    +  "' type='button' onclick=lw(this.value)  /> </td></tr>"

print "</table>"
