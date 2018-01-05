#!/usr/bin/python2

import cgi 
import commands
import os

print "content-type: text/html"
print



n_ip = cgi.FormContent()['n_ip'][0]

a = '''---
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
      src: "/hadoop/hdfs-site.xml"
      dest: "/etc/hadoop/"
   - name: "namenode format"
     command: "hadoop namenode -format"
   - name: "hadoop namenode service start"
     command: "hadoop-daemon.sh start namenode"

'''.format(n_ip)

c = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/hadoop_namenode</value>

</property>


</configuration>
'''

f2 = open('/hadoop/hdfs-site.xml', 'w')
f2.write(c)
f2.close()

f = open('/finalpart1/namenode.yml', 'w')
f.write(a)
f.close()

c = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}</value>

</property>


</configuration>
'''.format(n_ip)

f3 = open('/hadoop/core-site.xml', 'w')
f3.write(c)
f3.close()


a = commands.getstatusoutput("sudo ansible-playbook /finalpart1/namenode.yml")


if a[0] == 0:
	print "all done"
else:
	print "<pre>"
	print a[1]
	print "</pre>"












