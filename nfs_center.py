#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"
print 

c_IP = cgi.FormContent()['center'][0]
s_IP = cgi.FormContent()['server'][0]
size = cgi.FormContent()['size'][0]
print c_IP
print s_IP

def fileCopy():
	a = '''---
- hosts: {0}
  tasks:
   - package:
      name: "nfs-utils"
      state: present
   - file:
      path: "/share"
      state: directory
   - lvol:
      vg: "vg1"
      lv: "nfs1"
      size: '{1}g'
      state: present
   - filesystem:
      fstype: ext4
      dev: '/dev/vg1/nfs1'
   - mount:
      path: '/share'
      src: '/dev/vg1/nfs1'
      fstype: ext4
      fstab: '/etc/fstab'
      state: mounted
   - copy:
      src: "/finalpart1/sample.html"
      dest: "/share"
   - fetch:
      src: "/etc/exports"
      dest: "/finalpart1/"
      flat: yes
'''.format(c_IP, size)

	f = open('/finalpart1/nfs.yml','w')
	f.write(a)
	f.close()


def nfsSetup():
	b = '''---
- hosts: {}
  tasks:
   
   - copy:
      src: "/finalpart1/exports"
      dest: "/etc/"
      force: yes
   - service:
      name: "nfs"
      state: restarted

'''.format(c_IP)
	f1 = open('/finalpart1/nfs_1.yml','w')
	f1.write(b)
	f1.close()


def finalSetup():
	c = '''---
- hosts: {0}
  tasks:
   - package:
      name: "httpd"
      state: present
   - file:
      path: "/content"
      state: directory
   - copy:
      src: "/finalpart1/content.conf"
      dest: "/etc/httpd/conf.d/"
      force: yes
   - name: "mounting"
     command: 'mount {1}:/share /content' 
   - service:
      name: "httpd"
      state: restarted
      
'''.format(s_IP, c_IP)
	f2 = open('/finalpart1/nfs_web_server.yml','w')
	f2.write(c)
	f2.close()


fileCopy()

print "here"


nfsSetup()
print "done i think"

finalSetup()
print "<pre>"
if commands.getstatusoutput("sudo ansible-playbook /finalpart1/nfs.yml")[0] == 0:
	d = '''/share  {}\n'''.format(s_IP)
	f3 = open('/finalpart1/exports', 'a')
	f3.write(d)
	f3.close()
	print "done"
else:
	print "not ok"


print "done"
print commands.getoutput("sudo ansible-playbook /finalpart1/nfs_1.yml")
print "done"
print commands.getoutput("sudo ansible-playbook /finalpart1/nfs_web_server.yml")

print "done"



print "</pre>"



