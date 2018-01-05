#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print


a =  cgi.FormContent()

n_ip = a['n_ip']

b = []

del a['n_ip']
for i in a.keys():
	for j in a[i]:
		b.append(j)

print  b[0].split("\n")[0]

print "<pre>"
		

for i in range(1):
	print b[i]
	k = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{}:9001</value>

</property>

</configuration>



'''.format(b[0].split("\n")[0])
	f = open('/hadoop/mapred-site.xml', 'w')
	f.write(k)
	f.close()
	print "1 step"
	h = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>



'''.format(n_ip[0])
	f = open('/hadoop/core-site.xml', 'w')
	f.write(h)
	f.close()
	print "2 step"
	g = '''---
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

   - name: "hadoop job tracker service start"
     command: "hadoop-daemon.sh start jobtracker"


'''.format(b[i])
	f = open("/finalpart1/job.yml", 'w')
	f.write(g)
	f.close()
	print "3 step"
	if commands.getstatusoutput("sudo ansible-playbook /finalpart1/job.yml")[0] == 0:
		print "job tracker on air "
	else:
		print "sorry try to contact me on abc@ceo"


print "task"
for i in range(1, len(b)):
	h = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>hdfs://{}:9001</value>

</property>

</configuration>



'''.format(b[0].split("\n")[0])
	f = open('/hadoop/mapred-site.xml', 'w')
	f.write(h)
	f.close()

	print "1 step"
	g = '''---
- hosts: {0}
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
      src: "/hadoop/mapred-site.xml"
      dest: "/etc/hadoop/"
  
   - name: "hadoop task trakcer service start"
     command: "hadoop-daemon.sh start tasktracker"


'''.format(b[i])

	f = open("/finalpart1/task.yml", 'w')
	f.write(g)
	f.close()

	if commands.getstatusoutput("sudo ansible-playbook /finalpart1/task.yml")[0] == 0:
		print "task tracker running on "+b[i]
	else:
		print "contact to copyright holder "
	




