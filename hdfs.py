#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print


a =  cgi.FormContent()
size = a['lv']
b = []
del a['lv']
for i in a.keys():
	for j in a[i]:
		b.append(j)

print "<pre>"
		
print "namenode"
for i in range(1):
	print b[i]
	k = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/hadoop_namenode</value>

</property>

</configuration>



'''
	f = open('/hadoop/hdfs-site.xml', 'w')
	f.write(k)
	f.close()

	h = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>



'''.format(b[i].split("\n")[0])
	f = open('/hadoop/core-site.xml', 'w')
	f.write(h)
	f.close()
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
      src: "/hadoop/hdfs-site.xml"
      dest: "/etc/hadoop/"
   - name: "namenode format"
     command: "hadoop namenode -format"
   - name: "hadoop namenode service start"
     command: "hadoop-daemon.sh start namenode"


'''.format(b[i])
	f = open("/finalpart1/namenode.yml", 'w')
	f.write(g)
	f.close()

	print commands.getoutput("sudo ansible-playbook /finalpart1/namenode.yml")


print "datanode"
for i in range(1, len(b)):
	h = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>



'''.format(b[i].split("\n")[0])
	f = open('/hadoop/hdfs-site.xml', 'w')
	f.write(h)
	f.close()

	k = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/hadoop_datanode</value>

</property>

</configuration>



'''
	f = open('/hadoop/core-site.xml', 'w')
	f.write(k)
	f.close()

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
      src: "/hadoop/core-site.xml"
      dest: "/etc/hadoop/"
   - copy:
      src: "/hadoop/hdfs-site.xml"
      dest: "/etc/hadoop/"
   - lvol:
      vg: "vg1"
      lv: "lv1"
      size: "{1}g"
   - filesystem:
      fstype: ext4
      dev: "/dev/vg1/lv1"
   - file:
      path: "/hadoop_datanode"
      state: directory
   - mount:
      path: "/hadoop_datanode"
      src: "/dev/vg1/lv1"
      fstype: ext4
      state: mounted
   - name: "hadoop datanode service start"
     command: "hadoop-daemon.sh start datanode"


'''.format(b[i], size[0])

	f = open("/finalpart1/datanode.yml", 'w')
	f.write(g)
	f.close()

	print commands.getoutput("sudo ansible-playbook /finalpart1/datanode.yml")
	

print "size is {}".format(size[0])

print "</pre>"






