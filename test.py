#!/usr/bin/python  
#coding=gbk  
import smtplib  
from email.mime.text import MIMEText  
from urllib.request import urlopen    
  

f=urlopen('http://www.baidu.com')  
msg=MIMEText(f.read(),'html','utf-8')  
msg['Subject']='this is a test from python'  
msg['From']='from@163.com'  
msg['To']='to@qq.com'  
  
  
smtp=smtplib.SMTP()  
smtp.connect("smtp.163.com","25")  
smtp.login('from','password')  
smtp.sendmail('from@163.com','to@qq.com',msg.as_string())  
smtp.quit()  
