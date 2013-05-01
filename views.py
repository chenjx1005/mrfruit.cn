#!/usr/bin/env python
#coding=utf-8
import sys
import copy
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from werkzeug import secure_filename
from datetime import timedelta,date
from mail import newmail,sendmail,sendmailto
import xlwt
import time
from fruit2 import app,alipayTool


def connect_db():#连接数据åﾺ?
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		
		phone=request.form['phone']
		cur=g.db.execute('select tel,id,name,campus,building,room,score,mail from users where tel="'+phone+'"')
		row=cur.fetchall()
		if not row==[]:
			if request.form['stuid'] != str(row[0][1]):
				error = 'wrong id'
			else:
				session['logged_in'] = True
				session['name']=row[0][2]
				session['campus']=row[0][3]
				session['building']=row[0][4]
				session['room']=row[0][5]
				session['score']=row[0][6]
				session['mail']=row[0][7]
				session['phone'] = request.form['phone']
				session['stuid'] = request.form['stuid']
				return redirect(url_for('order'))
		else:
			error = 'register before login~'
	return render_template("log.html",error=error)

@app.route('/edit',methods=["POST","GET"])
def edit():
	if not session.get('logged_in'):
        	return redirect(url_for('log'))
	if request.method=='POST':
		building=request.form['address2']
		if 'address22' in request.form:
			building+=request.form['address22']
		building+="舍"
		try:
			g.db.execute('update users set mail=?,name=?,campus=?,building=?,room=? where tel=?',[request.form['email'],request.form['name'],request.form['address'],building,request.form['address3'],session['phone']])
			g.db.commit()
		except :
			flash('edit fail')
			return render_template("edit.html")
		else:
			session['name']=request.form['name']
			session['campus']=request.form['address']
			session['building']=building
			session['room']=request.form['address3']
			session['mail']=request.form['email']
		return redirect(url_for('order'))
	return render_template("edit.html")

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('log'))

@app.route('/changeadd',methods=['POST'])
def changeadd():
	g.db.execute('update users set name=?,campus=?,building=?,room=? where tel=?',[request.form['name'],request.form['address'],
	request.form['address2'],request.form['address3'],session['phone']])
	g.db.commit()
	#cur=g.db.execute('select * from orders where tel=?,name=?,campus=?,building=?,room=?',[session['phone'],request.form['name'],request.form['address'],
	#request.form['address2'],request.form['address3']])
	#row=cur.fetchall()
		#if not row==[]:
			
	session['name']=request.form['name']
	session['campus']=request.form['address']
	session['building']=request.form['address2']
	session['room']=request.form['address3']
	return redirect(url_for('order'))

@app.route('/',methods=['GET', 'POST'])
def order():
	if not session.get('logged_in'):
        	return redirect(url_for('log'))
	cur=g.db.execute('select score from users where tel=?',[session['phone']])
	session['score']=cur.fetchone()[0]
	a=session['score']
	show=[1,1,1,1,1]
	price=[0,0,0,0,0]
	cur=g.db.execute('select * from fruits order by f_id')
	row=cur.fetchall()
	
	cur1=g.db.execute('select f_id,numbers,re,f_name,price from orders where weekday=1 and tel=? and time>? order by f_id',[session['phone'],str(date.today())])
	row1=cur1.fetchall()
	#cur1=g.db.execute('select * from orders where weekday=1 and re=1 and tel=? and time>?',[session['phone'],str(date.today())])
	#rowm=cur1.fetchall()
	if not row1==[] and row1[0][2]==1:
		show[0]=0
	if row1==[]:
		row1=g.db.execute('select f_id,0,0,f_name,price from fruits').fetchall()
	for i in row1:		
		price[0]=price[0]+i[1]*i[4]
		
	cur2=g.db.execute('select f_id,numbers,re,f_name,price from orders where weekday=2 and tel=? and time>? order by f_id',[session['phone'],str(date.today())])
	row2=cur2.fetchall()
	if not row2==[] and row2[0][2]==1:
		show[1]=0
	if row2==[]:
		row2=g.db.execute('select f_id,0,0,f_name,price from fruits').fetchall()
	for i in row2:		
		price[1]=price[1]+i[1]*i[4]
	
	cur3=g.db.execute('select f_id,numbers,re,f_name,price from orders where weekday=3 and tel=? and time>? order by f_id',[session['phone'],str(date.today())])
	row3=cur3.fetchall()
	#cur1=g.db.execute('select * from orders where weekday=3 and re=1 and tel=? and time>?',[session['phone'],str(date.today())])
	#roww=cur1.fetchall()
	if not row3==[] and row3[0][2]==1:
		show[2]=0
	if row3==[]:
		row3=g.db.execute('select f_id,0,0,f_name,price from fruits').fetchall()
	for i in row3:		
		price[2]=price[2]+i[1]*i[4]
		
	cur4=g.db.execute('select f_id,numbers,re,f_name,price from orders where weekday=4 and tel=? and time>? order by f_id',[session['phone'],str(date.today())])
	row4=cur4.fetchall()
	if not row4==[] and row4[0][2]==1:
		show[3]=0
	if row4==[]:
		row4=g.db.execute('select f_id,0,0,f_name,price from fruits').fetchall()
	for i in row4:		
		price[3]=price[3]+i[1]*i[4]
		
	cur5=g.db.execute('select f_id,numbers,re,f_name,price from orders where weekday=5 and tel=? and time>? order by f_id',[session['phone'],str(date.today())])
	row5=cur5.fetchall()
	#cur1=g.db.execute('select * from orders where weekday=5 and re=1 and tel=? and time>?',[session['phone'],str(date.today())])
	#rowf=cur1.fetchall()
	if not row5==[] and row5[0][2]==1:
		show[4]=0
	if row5==[]:
		row5=g.db.execute('select f_id,0,0,f_name,price from fruits').fetchall()
	for i in row5:		
		price[4]=price[4]+i[1]*i[4]
	return render_template("order.html",row=row,row1=row1,row2=row2,row3=row3,row4=row4,row5=row5,price=price,show=show)

@app.route('/reg',methods=['GET', 'POST'])
def reg():
	if request.method=='POST':
		building=request.form['address2']
		if 'address22' in request.form and not request.form['address']=='yq':
			building+=request.form['address22']
		building+="舍"
		try:
			g.db.execute('insert into users values (?,?,?,?,0,?,?,?,0)',[request.form['phone'],request.form['stuid'],request.form['name'],
			request.form['email'],request.form['address'],request.form['address2'],request.form['address3']])
			g.db.commit()
		except :
			flash('phone number existed')
			return render_template("reg.html")
		else:
			session['logged_in'] = True
			session['phone'] = request.form['phone']
			session['stuid'] = request.form['stuid']
			session['name']=request.form['name']
			session['campus']=request.form['address']
			session['building']=building
			session['room']=request.form['address3']
			session['mail']=request.form['email']
			#g.db.execute('insert into orders values(?,0,0,1,"0",?,?,?,?,0)',[request.form['phone'],request.form['name'],request.form['address']
			#,request.form['address2'],request.form['address3']])
		return redirect(url_for('order'))
	return render_template("reg.html")

@app.route('/msg')
def msg():
	if not session.get('logged_in'):
		return redirect(url_for('log'))
	cur=g.db.execute('select time,me,time2,fruit from msg where tel=? order by time desc',[session['phone']])
	row=cur.fetchall()
	return render_template("msg.html",row=row)

@app.route('/newmsg',methods=['POST'])
def newmsg():
	s="tel:"+session['phone']+"  name:"+session['name']+"   studyid:"+session['stuid']+"   email:"+session['mail']+"   message:"+request.form['txt']
	print s
	#newmail(s)
	g.db.execute('insert into msg (tel,time,me,time2,fruit) values(?,datetime("now","localtime"),?,null,null)',[session['phone'],request.form['txt']])
	g.db.commit()
	#flash('we have recieved message~')
	return redirect(url_for('msg'))
	
@app.route('/history',methods=['POST','GET'])
def history():
	row=[]
	price=[]
	if request.method=="POST":
		time1=request.form['year1']+'-'+request.form['month1']+'-'+request.form['day1']
		time2=request.form['year2']+'-'+request.form['month2']+'-'+request.form['day2']
		cur=g.db.execute("select time from orders where re=1 and numbers>0 and tel=? and time>=? and time<=? group by time order by time desc",[session['phone'],time1,time2])
		time=cur.fetchall()
		
		if time==[]:
			flash("您查询的日期内没有订单～")
		
		for i in time:
			cur=g.db.execute("select time,weekday,f_name,numbers,price,id from orders where re=1 and numbers>0 and tel=? and time=?",[session['phone'],i[0]])
			r=cur.fetchall()
			p=0
			for j in r:
				p=p+j[3]*j[4]
			price.append(p)
			row.append(r)
		#raise RuntimeError
	return render_template("history.html",row=row,price=price)
	
@app.route('/receive/<id>')
def receive(id):
	g.db.execute("insert into receive values(?)",[id])
	g.db.commit()
	flash("已收到！我们会尽快联系你～")
	return redirect(url_for("history"))
	
@app.route('/questions')
def questions():
	return render_template("questions.html")	

@app.route('/add1',methods=['POST'])
def add1():
	w=date.isoweekday(date.today())
	setime=date.today()+timedelta(days=(8-w))
	s=str(setime)
	time=s[:4]+s[5:7]+s[8:]
	no=session['phone']+time
	cur=g.db.execute('select * from fruits order by f_id')
	rowf=cur.fetchall()
	g.db.execute("delete from orders where id=?",[no])
	g.db.commit()
	for i in request.form:
		g.db.execute('insert into orders values(?,?,?,?,1,?,0,?,?)',[no,session['phone'],int(i),int(request.form[i]),s,rowf[int(i)-1][1],rowf[int(i)-1][2]])	
		g.db.commit()
	return redirect(url_for("order"))
	
@app.route('/add2',methods=['POST'])
def add2():
	w=date.isoweekday(date.today())
	if w==2:
		setime=date.today()+timedelta(days=7)
	else:
		setime=date.today()+timedelta(days=((9-w)%7))
	s=str(setime)
	time=s[:4]+s[5:7]+s[8:]
	no=session['phone']+time
	cur=g.db.execute('select * from fruits order by f_id')
	rowf=cur.fetchall()
	g.db.execute("delete from orders where id=?",[no])
	g.db.commit()
	for i in request.form:
		g.db.execute('insert into orders values(?,?,?,?,2,?,0,?,?)',[no,session['phone'],int(i),int(request.form[i]),s,rowf[int(i)-1][1],rowf[int(i)-1][2]])		
		g.db.commit()
	return redirect(url_for("order"))
	
@app.route('/add3',methods=['POST'])
def add3():
	w=date.isoweekday(date.today())
	if w==3:
		setime=date.today()+timedelta(days=7)
	else:
		setime=date.today()+timedelta(days=((10-w)%7))	
	s=str(setime)
	time=s[:4]+s[5:7]+s[8:]
	no=session['phone']+time
	cur=g.db.execute('select * from fruits order by f_id')
	rowf=cur.fetchall()
	g.db.execute("delete from orders where id=?",[no])
	g.db.commit()
	for i in request.form:
		g.db.execute('insert into orders values(?,?,?,?,3,?,0,?,?)',[no,session['phone'],int(i),int(request.form[i]),s,rowf[int(i)-1][1],rowf[int(i)-1][2]])	
		g.db.commit()
	return redirect(url_for("order"))
	
@app.route('/add4',methods=['POST'])
def add4():
	w=date.isoweekday(date.today())
	if w==4:
		setime=date.today()+timedelta(days=7)
	else:
		setime=date.today()+timedelta(days=((11-w)%7))
	s=str(setime)
	time=s[:4]+s[5:7]+s[8:]
	no=session['phone']+time
	cur=g.db.execute('select * from fruits order by f_id')
	rowf=cur.fetchall()
	g.db.execute("delete from orders where id=?",[no])
	g.db.commit()
	for i in request.form:
		g.db.execute('insert into orders values(?,?,?,?,4,?,0,?,?)',[no,session['phone'],int(i),int(request.form[i]),s,rowf[int(i)-1][1],rowf[int(i)-1][2]])		
		g.db.commit()
	return redirect(url_for("order"))
	
@app.route('/add5',methods=['POST'])
def add5():
	w=date.isoweekday(date.today())
	if w==5:
		setime=date.today()+timedelta(days=7)
	else:
		setime=date.today()+timedelta(days=((12-w)%7))	
	s=str(setime)
	time=s[:4]+s[5:7]+s[8:]
	no=session['phone']+time
	cur=g.db.execute('select * from fruits order by f_id')
	rowf=cur.fetchall()
	g.db.execute("delete from orders where id=?",[no])
	g.db.commit()
	for i in request.form:
		g.db.execute('insert into orders values(?,?,?,?,5,?,0,?,?)',[no,session['phone'],int(i),int(request.form[i]),s,rowf[int(i)-1][1],rowf[int(i)-1][2]])		
		g.db.commit()
	return redirect(url_for("order"))
	
@app.route('/re',methods=['GET','POST'])
def re():
	#g.db.execute('update orders set re=1 where tel=?  and name=? and campus=? and building=? and room=? and time>?',
	#[session['phone'],session['name'],session['campus'],session['building'],session['room'],str(date.today())])	
	#g.db.commit()
	row=[]
	price=[]
	cur=g.db.execute("select time from orders where re=0 and numbers>0 and tel=? and time>? group by time order by time desc",[session['phone'],date.today()])
	ti=cur.fetchall()
	id=""	
	for i in ti:
		cur=g.db.execute("select time,weekday,f_name,numbers,price,id from orders where re=0 and numbers>0 and tel=? and time=?",[session['phone'],i[0]])
		r=cur.fetchall()
		p=0
		id+="_"+r[0][5]
		for j in r:
			p=p+j[3]*j[4]
		price.append(p)
		row.append(r)
	total_fee=0
	for i in price:
		total_fee+=i
	no=session['phone']+time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
	params={
       'out_trade_no':no,
       'subject'     :"NO"+no,
       'body'        :"水果"+id,
	   'logistics_type':'POST',
	   'logistics_fee':'0',
	   'logistics_payment':'BUYER_PAY',
	   'price':str(total_fee),
	   'quantity':'1',
       'total_fee'   :str(total_fee),
	   'receive_name':session['name'],
	   'receive_address':session['campus']+session['building']+session['room'],
	   'receive_zip':'310013',
	   'receive_mobile':session['phone']
	}
	payhtml=alipayTool.createPayForm(params)
	#将payhtml写到页面，这是个包含有提交按钮的表单
	
	
	#flash('Your orders have been submited~~')
	return render_template("pay.html",payhtml=payhtml,row=row,price=price)

@app.route('/test',methods=['POST'])
def test():
	f=request.form
	rlt=alipayTool.notifiyCall(f,verify=True)
	if rlt=='success':
		no=f['body'].split('_')
		for i in no[1:]:
			g.db.execute('update orders set re=1 where id=?',[i])
		g.db.execute('update users set score=score+? where tel=?',[int(float(f['total_fee'])*10),f['receive_mobile']])
		g.db.commit()
	return rlt

@app.route('/test2',methods=['GET'])
def test2():
	f=request.args
	rlt=alipayTool.notifiyCall(f,verify=True)
	#raise RuntimeError
	if rlt=='success':
		return redirect(url_for('order'))
	else:
		return redirect(url_for('msg'))		

@app.route('/weekly/<tel>')
def weekly(tel):
	setime=date.today()+timedelta(days=-7)
	cur=g.db.execute('select f_name,sum(numbers),price from orders inner join fruits on orders.f_id=fruits.f_id where orders.tel=? and re=1 and numbers>0 and time>? and time<? group by orders.f_id',[tel,str(setime),str(date.today())])
	row=cur.fetchall()
	price=0
	for i in row:
		price=price+i[1]*i[2]
	return render_template('weekly.html',row=row,price=price)

@app.route('/daily/<tel>')
def daily(tel):
	setime=date.today()+timedelta(days=1)
	cur=g.db.execute('select f_name,sum(numbers),price from orders inner join fruits on orders.f_id=fruits.f_id where orders.tel=? and numbers>0 and re=1 and time=? group by orders.f_id',[tel,str(setime)])
	row=cur.fetchall()
	price=0
	for i in row:
		price=price+i[1]*i[2]
	return render_template('daily.html',row=row,price=price)

@app.route('/admin')
def admin():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	return render_template('admin.html')
	
@app.route('/excel1')
def excel1():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	#表格1，水果种类，总数量，时间	
	cur=g.db.execute('select f_name,sum(numbers),time from orders where re=1 and time>=? and numbers>0 group by time,f_name',[str(date.today())])
	row=cur.fetchall()
	file = xlwt.Workbook(encoding="utf-8") 
	sheet = file.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet.write(0,0,"水果")
	sheet.write(0,1,"数量")
	sheet.write(0,2,"时间")
	p=1
	for i in row:
		for j in (range(3)):
			sheet.write(p,j,i[j])
		p=p+1
	file.save('/home/mrfruit/fruit2/static/1_fruit_sum_time.xls')
	return '<a href="/static/1_fruit_sum_time.xls">下载</a>'
@app.route('/excel2')
def excel2():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	#表格2
	cur=g.db.execute('select users.tel,name,campus,building,room,f_name,numbers,time from users inner join orders on users.tel=orders.tel where re=1 and numbers>0 and time>=? order by time,campus,building,room,name',[str(date.today())])
	row=cur.fetchall()
	file = xlwt.Workbook(encoding="utf-8") 
	sheet = file.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet.write(0,0,"电话")
	sheet.write(0,1,"姓名")
	sheet.write(0,2,"校区")
	sheet.write(0,3,"宿舍楼")
	sheet.write(0,4,"寝室号")
	sheet.write(0,5,"水果")
	sheet.write(0,6,"数量")
	sheet.write(0,7,"时间")
	
	p=1
	for i in row:
		for j in (range(8)):
			sheet.write(p,j,i[j])
		p=p+1
	file.save('/home/mrfruit/fruit2/static/2_user_position_fruit.xls')
	return '<a href="/static/2_user_position_fruit.xls">下载</a>'
	
@app.route('/excel3')
def excel3():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	cur=g.db.execute('select campus,f_name,sum(numbers),time from orders inner join users on orders.tel=users.tel where re=1 and time>=? and numbers>0 group by time,f_name,campus order by time,campus',[str(date.today())])
	row=cur.fetchall()
	file = xlwt.Workbook(encoding='utf-8') 
	sheet = file.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet.write(0,0,"校区")
	sheet.write(0,1,"水果")
	sheet.write(0,2,"数量")
	sheet.write(0,2,"时间")
	p=1
	for i in row:
		for j in (range(4)):
			sheet.write(p,j,i[j])
		p=p+1
	file.save('/home/mrfruit/fruit2/static/3_campus_fruit_sum_time.xls')
	return '<a href="/static/3_campus_fruit_sum_time.xls">下载</a>'

@app.route('/excel4')	
def excel4():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	cur=g.db.execute('select f_name,sum(numbers),price,sum(numbers)*price from orders where re=1 and time=? and numbers>0 group by time,f_name',[str(date.today()+timedelta(days=-1))])
	row=cur.fetchall()
	file = xlwt.Workbook(encoding='utf-8') 
	sheet = file.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet.write(0,0,"水果")
	sheet.write(0,1,"数量")
	sheet.write(0,2,"单价")
	sheet.write(0,3,"总额")
	p=1
	for i in row:
		for j in (range(4)):
			sheet.write(p,j,i[j])
		p=p+1
	file.save('/home/mrfruit/fruit2/static/4_fruit_summoney.xls')
	return '<a href="/static/4_fruit_summoney.xls">下载</a>'
	
@app.route('/excel5')
def excel5():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	#表格2
	cur=g.db.execute('select users.tel,name,sum(numbers*price) from users inner join orders on users.tel=orders.tel where re=1 and numbers>0 and time=? group by users.tel',[str(date.today()+timedelta(days=-1))])
	row=cur.fetchall()
	file = xlwt.Workbook(encoding="utf-8") 
	sheet = file.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet.write(0,0,"电话")
	sheet.write(0,1,"姓名")
	sheet.write(0,2,"总金额")
	
	p=1
	for i in row:
		for j in (range(3)):
			sheet.write(p,j,i[j])
		p=p+1
	file.save('/home/mrfruit/fruit2/static/5_user_money.xls')
	return '<a href="/static/5_user_money.xls">下载</a>'
	
@app.route('/excel6')
def excel6():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	#表格2
	cur=g.db.execute('''select orders.tel,name from orders inner join users on orders.tel=users.tel where time<=? and time>=?
	except select orders.tel,name from orders inner join users on orders.tel=users.tel where time>=?''',[str(date.today()+timedelta(days=-14)),str(date.today()+timedelta(days=-28)),str(date.today()+timedelta(days=-14))])
	row=cur.fetchall()
	file = xlwt.Workbook(encoding="utf-8") 
	sheet = file.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet.write(0,0,"电话")
	sheet.write(0,1,"姓名")
	
	p=1
	for i in row:
		for j in (range(2)):
			sheet.write(p,j,i[j])
		p=p+1
	file.save('/home/mrfruit/fruit2/static/6_user.xls')
	return '<a href="/static/6_user.xls">近两周没订_再上两周订过</a>'
	
@app.route('/excel7')
def excel7():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	#表格2
	cur=g.db.execute('''select orders.tel,name from orders inner join users on orders.tel=users.tel where time>=?
	except select orders.tel,name from orders inner join users on orders.tel=users.tel where time>=? and time<=?''',[str(date.today()+timedelta(days=-14)),str(date.today()+timedelta(days=-28)),str(date.today()+timedelta(days=-14))])
	row=cur.fetchall()
	file = xlwt.Workbook(encoding="utf-8") 
	sheet = file.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet.write(0,0,"电话")
	sheet.write(0,1,"姓名")
	
	p=1
	for i in row:
		for j in (range(2)):
			sheet.write(p,j,i[j])
		p=p+1
	file.save('/home/mrfruit/fruit2/static/7_user.xls')
	return '<a href="/static/7_user.xls">最近两周新订</a>'
	
	
@app.route('/adminlog',methods=['GET','POST'])
def adminlog():
	if request.method=='POST':
		if request.form['name']=="admin" and request.form['password']=="mrfruit123":
			session['admin']=True
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('adminlog'))
	else:
		return render_template('adminlog.html')
		
@app.route('/admindomsg',methods=['GET','POST'])
def admindomsg():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	if request.method=='POST':
		g.db.execute('update msg set time2=datetime("now","localtime"),fruit=? where id=?',[request.form['re'],request.form['id']])
		g.db.commit()
		return redirect(url_for('admindomsg'))
	else:
		row=g.db.execute('select id,tel,time,me from msg where fruit is null order by time desc').fetchall()
	return render_template("admindomsg.html",row=row)

@app.route('/showmsg')
def showmsg():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	row=g.db.execute('select * from msg where time2 is not null order by time desc').fetchall()
	s="<a href='/admindomsg'>显示未处理留言</a>"
	for i in row:
		s+='<p>id:'+str(i[0])+"</p>"+'<p>tel:'+i[1]+'</p>'+'<p>time:'+i[2]+'</p>'+'<p>'+i[3]+'</p>'+'<p>    retime:'+i[4]+'</p>'+'<p>    re'+i[5]+'</p><hr>'
	return s

@app.route('/showreceive')
def showreceive():
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	row=g.db.execute('select orders.id,tel,time from receive inner join orders on receive.id=orders.id group by orders.id').fetchall()
	s=""
	for i in row:
		s+='<p>订单编号：'+i[0]+'  联系电话：'+i[1]+'   时间：'+i[2]+'</p><a href="/doreceive/'+i[0]+'">已处理</a><hr>'
	return s

@app.route('/doreceive/<id>')
def doreceive(id):
	if not session.get('admin'):
		return redirect(url_for('adminlog'))
	g.db.execute("delete from receive where id=?",[id])
	g.db.commit()
	return redirect(url_for("showreceive"))
	
@app.route('/adminlogout')
def adminlogout():
	session.pop('admin', None)
	return redirect(url_for('adminlog'))

@app.route('/mail_to_users')
def mailtousers():
	cur=g.db.execute('select tel,mail from users')
	row=cur.fetchall()
	for i in row:
		sendmail(i)
	flash('this week orders mails finished~')
	return redirect(url_for('admin'))
@app.route('/mail_tomorrow')
def tomorrow():
	cur=g.db.execute('select tel,mail from users')
	row=cur.fetchall()
	for i in row:
		sendmailto(i)
	flash('tomorrow orders mails finished~')
	return redirect(url_for('admin'))