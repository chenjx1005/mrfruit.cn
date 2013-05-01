#!/usr/bin/env python3
#coding: utf-8 
import smtplib 
from email.mime.text import MIMEText 
from email.header import Header 
  


def newmail(newmsg):  
	sender = 'meet_mrfruit@163.com' 
	receiver = '574959828@qq.com' 
	subject = 'mrfruit users message' 
	smtpserver = 'smtp.163.com' 
	username = 'meet_mrfruit' 
	password = 'mrfruit4142'
	msg = MIMEText(newmsg,'plain','utf-8')#中文需参数‘utf-8’，单字节字符不需�?
	msg['Subject'] = Header(subject, 'utf-8') 
  
	smtp = smtplib.SMTP() 
	smtp.connect('smtp.163.com') 
	smtp.login(username, password) 
	smtp.sendmail(sender, receiver, msg.as_string()) 
	smtp.quit()

def sendmail(row):
	sender = 'meet_mrfruit@163.com' 
	receiver = row[1] 
	subject = '您在mrfruit的本周订单～' 
	smtpserver = 'smtp.163.com' 
	username = 'meet_mrfruit' 
	password = 'mrfruit4142'
	newmsg="您本周在mrfruit的水果订单已经生成，点击此链接查看：<br>"+"http://42.121.2.44:8888/weekly/"+row[0]
	msg = MIMEText(newmsg,'html','utf-8')#中文需参数‘utf-8’，单字节字符不需�?
	msg['Subject'] = Header(subject, 'utf-8') 
  
	smtp = smtplib.SMTP() 
	smtp.connect('smtp.163.com') 
	smtp.login(username, password) 
	smtp.sendmail(sender, receiver, msg.as_string()) 
	smtp.quit()
def sendmailto(row):
	sender = 'meet_mrfruit@163.com' 
	receiver = row[1] 
	subject = '您在mrfruit的明天订单～' 
	smtpserver = 'smtp.163.com' 
	username = 'meet_mrfruit' 
	password = 'mrfruit4142'
	newmsg="您在mrfruit订的水果明天就要到了，点击此链接查看�?br>"+"http://42.121.2.44:8888/daily/"+row[0]
	msg = MIMEText(newmsg,'html','utf-8')#中文需参数‘utf-8’，单字节字符不需�?
	msg['Subject'] = Header(subject, 'utf-8') 
  
	smtp = smtplib.SMTP() 
	smtp.connect('smtp.163.com') 
	smtp.login(username, password) 
	smtp.sendmail(sender, receiver, msg.as_string()) 
	smtp.quit()
	
