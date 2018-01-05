#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print

size = cgi.FormContent()['size'][0]
n1 = cgi.FormContent()['n1'][0]
n_ip = cgi.FormContent()['n_ip'][0]
lv = cgi.FormContent()['lv'][0]

main_ip = '192.168.43.174'
main_pas = 'nick'
doc_pas = 'nick'


#commands.getoutput("sudo docker run -dit --name hdfs1 -p 2200:22 centos:latest")

a = commands.getoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no {1} docker ps --latest".format(main_pas, main_ip))
b = a.split()[-1]


c=commands.getoutput("""sudo sshpass -p {0} ssh -o stricthostkeychecking=no {1} docker inspect {2} | jq '.[].NetworkSettings.Ports."22/tcp"[].HostPort'""".format(main_pas, main_ip, b))

d = int(c[1:-1])


print "<pre>"
if n1 == 'hdfs':
	for i in range(1):
		d+=1
		print "i'm here"
		commands.getoutput("sudo ansible {2} -m command -a 'docker run -dit --name hdfs{1} -p {1}:22 nick:v3'".format(i, d, main_ip))
		print "i'm here"
		ip1 = commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1}  docker inspect {0} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format('hdfs'+str(d), main_ip, main_pas))
		print "i'm here"
		port = commands.getoutput("""sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1} docker inspect {0} | jq '.[].NetworkSettings.Ports."22/tcp"[].HostPort'""".format('hdfs'+str(d), main_ip, main_pas))
		print "i'm here"

		docker = """---
- hosts: {0}
  tasks:
   - copy:
       src: "/hadoop/core-site.xml"
       dest: "/root/"
   - copy:
       src: "/hadoop/hdfs-site.xml"
       dest: "/root/"
   - name: "docker core copy"
     command: "docker cp /root/core-site.xml {1}:/etc/hadoop/"
   - name: "docker hdfs copy"
     command: "docker cp /root/hdfs-site.xml {1}:/etc/hadoop/"
   


""".format(main_ip, 'hdfs'+str(d))	
		f = open("/finalpart1/docker_namenode.yml", 'w')
		f.write(docker)	
		f.close()
		print "i'm here"
		core = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>




'''.format(ip1[1:-1])
		hdfs = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/{0}</value>

</property>


</configuration>

'''.format('hdfs'+str(d))
		f1 = open('/hadoop/hdfs-site.xml', 'w')
		f1.write(hdfs)
		f1.close()
		
		f = open("/hadoop/core-site.xml", 'w')
		f.write(core)
		f.close()
	
		commands.getoutput("sudo ansible-playbook /finalpart1/docker_namenode.yml")
		commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {0} -p {1} hadoop namenode -format".format(main_ip, port[1:-1], doc_pas))
		commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {0} -p {1} hadoop-daemon.sh start namenode".format(main_ip, port[1:-1], doc_pas))
	

	for i in range(1, int(size)):
		d+=1
		print "i'm here"

		d1 = '''---
- hosts: {1}
  tasks:
  - lvol:
     vg: "vg1"
     lv: "{0}"
     size: "{2}g"
  - filesystem:
     fstype: ext4
     dev: "/dev/vg1/{0}"
  - file:
     path: "/{0}"
     state: directory
  - mount:
     path: "/{0}"
     src: "/dev/vg1/{0}"
     fstype: ext4     
     state: mounted


'''.format('hdfs'+str(d), main_ip, lv)
		f = open("/finalpart1/datanode_docker.yml", 'w')
		f.write(d1)
		f.close()

		d2 = '''---
- hosts: {1}
  tasks:
  - copy:
      src: "/hadoop/core-site.xml"
      dest: "/root/data/"
  - copy:
      src: "/hadoop/hdfs-site.xml"
      dest: "/root/data/"
  - name: "docker hdfs copy"
    command: "docker cp /root/data/hdfs-site.xml {0}:/etc/hadoop/"
  - name: "docker core copy "
    command: "docker cp /root/data/core-site.xml {0}:/etc/hadoop/"


'''.format('hdfs'+str(d), main_ip)
		f1 = open('/finalpart1/datanode_docker_2.yml', 'w')
		f1.write(d2)
		f1.close()
		
		core = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{0}:10001</value>

</property>

</configuration>


'''.format(ip1[1:-1])

		hdfs = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/{0}</value>

</property>


</configuration>

'''.format('hdfs'+str(d))
		f1 = open('/hadoop/core-site.xml', 'w')
		f1.write(core)
		f1.close()

		f1 = open('/hadoop/hdfs-site.xml', 'w')
		f1.write(hdfs)
		f1.close()

		commands.getoutput("sudo ansible-playbook /finalpart1/datanode_docker.yml")
		commands.getoutput("sudo ansible {3} -m command -a 'docker run -dit --volume /{2}:/{2} --name hdfs{1} -p {1}:22 nick:v3'".format(i, d, 'hdfs'+str(d), main_ip))
		print "i'm here"
		ip = commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1}  docker inspect {0} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format('hdfs'+str(d), main_ip, main_pas))
		print "i'm here"
		port = commands.getoutput("""sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1} docker inspect {0} | jq '.[].NetworkSettings.Ports."22/tcp"[].HostPort'""".format('hdfs'+str(d), main_ip, main_pas))

		commands.getoutput("sudo ansible-playbook /finalpart1/datanode_docker_2.yml")
		commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {0} -p {1} hadoop-daemon.sh start datanode".format(main_ip, port[1:-1], doc_pas))


	print "Do you want to continue"

	



elif n1 == 'mapred':
	ips = []
	ports = []
	for i in range(1):
		d+=1
		commands.getoutput("sudo ansible {2} -m command -a 'docker run -dit --name hdfs{1} --hostname hdfs{1} -p {1}:22 nick:v3'".format(i, d, main_ip))
		print "i'm here"
		ip2 = commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1}  docker inspect {0} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format('hdfs'+str(d), main_ip, main_pas))
		ips.append("{0}  hdfs{1}".format(ip2[1:-1], str(d)))
		print "i'm here"
		port = commands.getoutput("""sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1} docker inspect {0} | jq '.[].NetworkSettings.Ports."22/tcp"[].HostPort'""".format('hdfs'+str(d), main_ip, main_pas))
		ports.append(str(d))
		print "i'm here"

		job = '''---
- hosts: {0}
  tasks:
   - copy:
      src: "/hadoop/core-site.xml"
      dest: "/root/"
   - copy:
      src: "/hadoop/mapred-site.xml"
      dest: "/root/"

   - name: "core file copy"
     command: "docker cp /root/core-site.xml {1}:/etc/hadoop/"
   - name: "mapred file copy"
     command: "docker cp /root/mapred-site.xml {1}:/etc/hadoop/"


'''.format(main_ip, 'hdfs'+str(d))

		core = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>

</property>

</configuration>



'''.format(n_ip)
		mapred = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{}:9001</value>

</property>

</configuration>



'''.format(ip2[1:-1])
		f = open("/finalpart1/docker_job.yml", 'w')
		f.write(job)
		f.close()

		f1 = open("/hadoop/core-site.xml", 'w')
		f1.write(core)
		f1.close()

		f2 = open("/hadoop/mapred-site.xml", "w")
		f2.write(mapred)
		f2.close()		
		
		commands.getoutput("sudo ansible-playbook /finalpart1/docker_job.yml")
		commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {0} -p {1} hadoop-daemon.sh start jobtracker".format(main_ip, port[1:-1], main_pas))
		commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {0} -p {1} hadoop-daemon.sh start jobtracker".format(main_ip, port[1:-1], main_pas))


	for i in range(1, int(size)):
		d+=1
		commands.getoutput("sudo ansible {2} -m command -a 'docker run -dit --name hdfs{1} --hostname hdfs{1} -p {1}:22 nick:v3'".format(i, d, main_ip))
		print "i'm here"
		ip = commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1}  docker inspect {0} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format('hdfs'+str(d), main_ip, main_pas))
		ips.append("{0}  hdfs{1}".format(ip[1:-1], str(d)))
		print "i'm here"
		port = commands.getoutput("""sudo sshpass -p {2} ssh -o stricthostkeychecking=no {1} docker inspect {0} | jq '.[].NetworkSettings.Ports."22/tcp"[].HostPort'""".format('hdfs'+str(d), main_ip, main_pas))
		ports.append(port[1:-1])
		print "i'm here"

		job = '''---
- hosts: {0}
  tasks:
   - copy:
      src: "/hadoop/mapred-site.xml"
      dest: "/root/"
   - name: "mapred file copy"
     command: "docker cp /root/mapred-site.xml {1}:/etc/hadoop/"


'''.format(main_ip, 'hdfs'+str(d))

		mapred = '''<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{}:9001</value>

</property>

</configuration>



'''.format(ip2[1:-1])
		f = open("/finalpart1/docker_task.yml", 'w')
		f.write(job)
		f.close()


		f2 = open("/hadoop/mapred-site.xml", "w")
		f2.write(mapred)
		f2.close()		
		
		commands.getoutput("sudo ansible-playbook /finalpart1/docker_task.yml")
		commands.getoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no {0} -p {1} hadoop-daemon.sh start tasktracker".format(main_ip, port[1:-1], doc_pas))
	print ports
	print ips

	for ip in ips:
		commands.getoutput("echo {} | cat >> /finalpart1/hosts".format(ip))
	print "i think i'm running"
	for i in range(len(ports)):
		commands.getoutput("sudo sshpass -p {0} scp -o stricthostkeychecking=no -P {1} /finalpart1/hosts {2}:/etc/".format(doc_pas, ports[i], main_ip))

	print "Do you want to continue"

	



else:
	print "you are out of way"


