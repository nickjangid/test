#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print

d_ip = cgi.FormContent()['d_ip'][0]
n_ip = cgi.FormContent()['n_ip'][0]


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
      src: "/hadoop/hdfs-site.xml"
      dest: "/etc/hadoop/"
   - lvol:
      vg: "vg1"
      lv: "lv1"
      size: "1g"
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

'''.format(d_ip)

b = '''
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>'''.format(n_ip.split("\n")[0])

c = '''
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/hadoop_datanode</value>

</property>


</configuration>
'''

f2 = open('/hadoop/hdfs-site.xml', 'w')
f2.write(c)
f2.close()

f = open('/finalpart1/datanode.yml', 'w')
f.write(a)
f.close()

f1 = open('/hadoop/core-site.xml', 'w')
f1.write(b)
f1.close()


a = commands.getstatusoutput("sudo ansible-playbook /finalpart1/datanode.yml")


if a[0] == 0:
	print "all done"
else:
	print "<pre>"
	print a[1]
	print "</pre>"









