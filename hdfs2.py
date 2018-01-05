#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print

a =  cgi.FormContent()
size = a['d_size']
b = []
del a['d_size']
for i in a.keys():
	for j in a[i]:
		b.append(j)

print b
		
print "namenode"

def namenode():
	a = '''---
- hosts: {}
  tasks:
   - copy:
      src: "/hadoop2"
      dest: "/root/hadoop"
   - package:
      name: "jdk"
      state: absent
   - package:
      name: "hadoop"
      state: absent
   - package: 
      name: "/root/hadoop/hadoop2/jdk-7u79-linux-x64.rpm"
      state: present
   - lineinfile: 
      path: "/root/.bashrc"
      line: "export JAVA_HOME=/usr/java/jdk1.7.0_79"
      state: present
   - lineinfile:
      path: "/root/.bashrc"
      line: "export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
   - file:
      path: "/hadoop2"
      state: directory
   - unarchive:
      src: "/root/hadoop/hadoop2/hadoop-2.6.4.tar.gz"
      dest: "/hadoop2/"
      remote_src: True
   - lineinfile:
      path: "/root/.bashrc"
      line: "export HADOOP_HOME=/hadoop2/hadoop-2.6.4"
   - lineinfile:
      path: "/root/.bashrc"
      line: "export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"
   - copy:
      src: "/hadoop2/core-site.xml"
      dest: "/hadoop2/hadoop-2.6.4/etc/hadoop/"
   - copy:
      src: "/hadoop2/hdfs-site.xml"
      dest: "/hadoop2/hadoop-2.6.4/etc/hadoop/"
   - name: "namenode format"
     command: "hdfs namenode -format"
   - name: "hadoop namenode service start"
     command: "hadoop-daemon.sh start namenode"
'''.format(b[0])
	f = open('/finalpart1/hdfs_namenode.yml', 'w')
	f.write(a)
	f.close()

	hdfs = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>file:/data/nn</value>

</property>

</configuration>
'''
	core = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>
'''.format(b[0])
	f = open('/hadoop2/hdfs-site.xml', 'w')
	f.write(hdfs)
	f.close()
	
	f = open('/hadoop2/core-site.xml', 'w')
	f.write(core)
	f.close()


def datanode(ip):
	print "i'm here"
	e = '''---
- hosts: {0}
  tasks:
   - copy:
      src: "/hadoop2"
      dest: "/root/hadoop"
   - package:
      name: "jdk"
      state: absent
   - package:
      name: "hadoop"
      state: absent
   - package: 
      name: "/root/hadoop/hadoop2/jdk-7u79-linux-x64.rpm"
      state: present
   - lineinfile: 
      path: "/root/.bashrc"
      line: "export JAVA_HOME=/usr/java/jdk1.7.0_79"
      state: present
   - lineinfile:
      path: "/root/.bashrc"
      line: "export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
   - file:
      path: "/hadoop2"
      state: directory
   - unarchive:
      src: "/root/hadoop/hadoop2/hadoop-2.6.4.tar.gz"
      dest: "/hadoop2/"
      remote_src: True
   - lineinfile:
      path: "/root/.bashrc"
      line: "export HADOOP_HOME=/hadoop2/hadoop-2.6.4"
   - lineinfile:
      path: "/root/.bashrc"
      line: "export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"
   - copy:
      src: "/hadoop2/core-site.xml"
      dest: "/hadoop2/hadoop-2.6.4/etc/hadoop/"
   - copy:
      src: "/hadoop2/hdfs-site.xml"
      dest: "/hadoop2/hadoop-2.6.4/etc/hadoop/"

   - lvol:
      vg: "vg1"
      lv: "lv1"
      size: "{1}g"
   - filesystem:
      fstype: ext4
      dev: "/dev/vg1/lv1"
   - file:
      path: "/data"
      state: directory
   - file:
      path: "/data/dn"
      state: directory

   - mount:
      path: "/data/dn"
      src: "/dev/vg1/lv1"
      fstype: ext4
      state: mounted
   - name: "namenode format"
     command: "hdfs namenode -format"
   - name: "hadoop namenode service start"
     command: "hadoop-daemon.sh start namenode"
   - name: "hadoop datanode service start"
     command: "hadoop-daemon.sh start datanode"
   - name: "hadoop mapred service start"
     command: "yarn-daemon.sh start resourcemanager"
   - name: "hadoop yarn service start"
     command: "yarn-daemon.sh start nodemanager"


'''.format(ip, size[0])
	f = open('/finalpart1/hdfs_datanode.yml', 'w')
	f.write(e)
	f.close()


	hdfs = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.name.dir</name>
<value>file:/data/nn</value>

</property>


<property>
<name>dfs.data.dir</name>
<value>file:/data/dn</value>

</property>

</configuration>
'''
	core = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>
'''.format(ip)
	f = open('/hadoop2/hdfs-site.xml', 'w')
	f.write(hdfs)
	f.close()
	
	f = open('/hadoop2/core-site.xml', 'w')
	f.write(core)
	f.close()

	mapred = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>

</property>

</configuration>
'''
	yarn = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>

</property>

</configuration>
'''
	f = open('/hadoop2/mapred-site.xml', 'w')
	f.write(mapred)
	f.close()
	
	f = open('/hadoop2/yarn-site.xml', 'w')
	f.write(yarn)
	f.close()



#namenode()

#print commands.getoutput("sudo ansible-playbook /finalpart1/hdfs_namenode.yml")

for i in range(len(b)):
	print b[i]



for j in range(len(b)):
	datanode(str(b[i]))
	print commands.getoutput("sudo ansible-playbook /finalpart1/hdfs_datanode.yml")
	print "runnig"

