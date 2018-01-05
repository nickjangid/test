#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print


n_ip = cgi.FormContent()['n_ip'][0]
ip = cgi.FormContent()['ip'][0]

a = '''
---
- hosts: {}
  tasks:
   - copy:
      src: "/hadoop"
      dest: "/root/hadoop"
   - package:
      name: "jdk"
      state: absent
   - package:
      name: "hadoop"
      state: absent
   - package: 
      name: "/root/hadoop/hadoop/jdk-7u79-linux-x64.rpm"
      state: present
   - name: "export java path_1"
     command: "echo 'export JAVA_HOME=/usr/java/jdk1.7.0_79' | cat >> /root/.bashrc"
   - name: "export java path_2"
     command: "echo 'export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH' | cat >> /root/.bashrc"
   - name: "hadoop install"
     command: "rpm -ivh /root/hadoop/hadoop/hadoop-1.2.1-1.x86_64.rpm --replacefiles"
   - copy:
      src: "/hadoop/core-site.xml"
      dest: "/etc/hadoop/"
   - copy:
      src: "/hadoop/mapred-site.xml"
      dest: "/etc/hadoop/"
   - name: "hadoop job trakcer service start"
     command: "hadoop-daemon.sh start jobtracker"

'''.format(ip)

b = '''
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{}:9001</value>

</property>


</configuration>
'''.format(n_ip.split("\n")[0])


f2 = open('/hadoop/mapred-site.xml', 'w')
f2.write(b)
f2.close()

f = open('/finalpart1/jobtracker.yml', 'w')
f.write(a)
f.close()


a = commands.getstatusoutput("sudo ansible-playbook /finalpart1/job.yml")


if a[0] == 0:
	print "all done"
else:
	print "<pre>"
	print a[1]
	print "</pre>"

