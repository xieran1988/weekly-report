#!/usr/bin/python
#coding:utf-8

import sys, struct
import smtplib, mimetypes, base64 
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage  

def docsub(s, args):
	for a,b in args:
		f = ( lambda x: x ) if type(a) == type('') else \
				( lambda x: ''.join([ '\\\'%.2x'%struct.unpack('B',i) for i in list(x.encode('gbk'))]) )
		s = str.replace(s, f(a), f(b))
	return s

l = [ i.strip() for i in sys.stdin.readlines() ]
if len(l) == 0:
	print 'Nothing to send'
	sys.exit(1)
no = l[0]
date = '%s-%s-%s'%(no[:4], no[4:6], no[6:])
items = [ i.decode('utf-8') for i in l[1:] ] + [ u' '] * 10

fileName = '/tmp/a.doc'
open(fileName, 'wb+').write(
	docsub(open('pat.doc').read(), [
	('recordnumber', 'WRPWG'+no),
	('recorddate', date),
	(u'条目一', items[0]),
	(u'条目二', items[1]),
	(u'条目三', items[2]),
	(u'条目四', items[3]),
	]))

def utf(s):
	return '=?utf-8?B?'+base64.encodestring(s).strip()+'?='

fromaddr = 'enliest@qq.com'
toaddrs  = [ 'zhanghaoscut@qq.com', 'fgliu@scut.edu.cn', 'enliest@qq.com' ]
subj = '周报_谢然_'+no
msg = MIMEMultipart()
msg['Subject'] = utf(subj)
msg['From'] = fromaddr
msg['To'] = ";".join(toaddrs)

ctype = 'application/octet-stream'  
maintype, subtype = ctype.split('/', 1)  
att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(fileName, 'rb'))[0], _subtype = subtype)  
att1.add_header('Content-Disposition', 'attachment', filename = utf(subj+'.doc'))
msg.attach(att1) 

server = smtplib.SMTP()
server.connect('smtp.qq.com')
server.login(open('user').read().strip(), open('pass').read().strip())
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg.as_string())
server.quit()

