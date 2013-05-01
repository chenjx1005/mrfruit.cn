#!/usr/bin/env python
#coding=utf-8
import sys
import copy
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from werkzeug import secure_filename
from datetime import timedelta,date
from mail import newmail,sendmail,sendmailto
import xlwt
import alipay
import time
# configuration
PATH='/home/mrfruit/fruit/'
DATABASE = PATH+'data.db'#数据库位çﾽ?
DEBUG = True
SECRET_KEY = 'test'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():#连接数据åﾺ?
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response
	
alipayTool=alipay.alipay(
                partner="2088302144896577",
                key="hugp0odb7elvw131cjla0s6x2aoxizqp",
                sellermail="18768114571",
                notifyurl="http://www.mrfruit.cn/test",
                returnurl="http://www.mrfruit.cn/test2",
                showurl=""
                )

@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		
		phone=request.form['phone']
		cur=g.db.execute('select tel,id,name,campus,building,room,score,mail from users where tel="'+phone+'"')
		row=cur.fetchall()
		if not row==[]:
			#if request.form['stuid'] != str(row[0][1]):
			if request.form['stuid'] != "000123":
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
		if 'address22' in request.form and not request.form['address']=='yq':
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
	cur=g.db.execute('select * from fruits order by f_id')
	fruits=cur.fetchall()
	return render_template("order.html",fruits=fruits)

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
		time1,time2=request.form['time1'].replace('/','-'),request.form['time2'].replace('/','-')
		time1=time1[6:]+'-'+time1[0:5]
		time2=time2[6:]+'-'+time2[0:5]
		cur=g.db.execute("select time from orders where re=1 and numbers>0 and tel=? and time>=? and time<=? group by time order by time desc",[session['phone'],time1,time2])
		time=cur.fetchall()
		
		if time==[]:
			flash("您查询的日期内没有订单～")
		
		for i in time:
			cur=g.db.execute("select time,weekday,f_name,sum(numbers),price,id,1 from orders where re=1 and numbers>0 and tel=? and time=? group by f_name",[session['phone'],i[0]])
			r=cur.fetchall()
			p=0
			for j in r:
				p=p+j[3]*j[4]
			price.append(p)
			row.append(r)
		#raise RuntimeError
	return render_template("history.html",row=row,price=price)
	
@app.route('/history1',methods=['POST'])
def history1():
	row=[]
	price=[]
	time1,time2=request.form['time1'].replace('/','-'),request.form['time2'].replace('/','-')
	time1=time1[6:]+'-'+time1[0:5]
	time2=time2[6:]+'-'+time2[0:5]
	cur=g.db.execute("select id from orders where re=1 and numbers>0 and tel=? and buytime>=? and buytime<=? group by id order by buytime desc",[session['phone'],time1,time2])
	id=cur.fetchall()	
		
	if id==[]:
		flash("您查询的日期内没有订单～")

	for i in id:
		cur=g.db.execute("select buytime,weekday,f_name,numbers,price,id,pay from orders where re=1 and numbers>0 and tel=? and id=?",[session['phone'],i[0]])
		r=cur.fetchall()
		p=0
		for j in r:
			p=p+j[3]*j[4]
		price.append(p)
		row.append(r)
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
	
@app.route('/re',methods=['GET','POST'])
def re():
	#g.db.execute('update orders set re=1 where tel=?  and name=? and campus=? and building=? and room=? and time>?',
	#[session['phone'],session['name'],session['campus'],session['building'],session['room'],str(date.today())])	
	#g.db.commit()
	f=request.form
	no=session['phone']+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	if request.method=="POST":
		g.db.execute('delete from orders where re=0 and tel=?',[session['phone']])
		g.db.commit()
		
		w=date.isoweekday(date.today())
		for key in f:
			weekday=int(key[0])
			f_id=int(key[2:])
			numbers=int(f[key])
			f_name,price=g.db.execute('select f_name,price from fruits where f_id=?',[f_id]).fetchall()[0]
			if weekday>w:
				setime=date.today()+timedelta(days=(weekday-w))
			else:
				setime=date.today()+timedelta(days=(7-w+weekday))
			g.db.execute('insert into orders values(?,?,?,?,?,?,?,?,?,?,?)',[no,session['phone'],f_id,numbers,weekday,setime,0,f_name,price,0,date.today()])
		g.db.commit()

	money=g.db.execute('select sum(price*numbers) from orders where pay=0 and re=1 and tel=?',[session['phone']]).fetchall()[0][0]
	if money:
		session['money']=float(money)
	else:
		session['money']=0
	row=[]
	price=[]
	cur=g.db.execute("select time from orders where re=0 and numbers>0 and tel=? and time>? group by time order by time",[session['phone'],date.today()])
	ti=cur.fetchall()
	for i in ti:
		cur=g.db.execute("select time,weekday,f_name,numbers,price,id from orders where re=0 and numbers>0 and tel=? and time=?",[session['phone'],i[0]])
		r=cur.fetchall()
		p=0
		for j in r:
			p=p+j[3]*j[4]
		price.append(p)
		row.append(r)
	total_fee=0
	for i in price:
		total_fee+=i
	params={
       'out_trade_no':no,
       'subject'     :"NO"+no,
       'body'        :"水果"+no,
	   'logistics_type':'POST',
	   'logistics_fee':'0',
	   'logistics_payment':'BUYER_PAY',
	   'price':str(total_fee+session['money']),
	   'quantity':'1',
       'total_fee'   :str(total_fee+session['money']),
	   'receive_name':session['name'],
	   'receive_address':session['campus']+session['building']+session['room'],
	   'receive_zip':'310013',
	   'receive_mobile':session['phone']
	}
	payhtml=alipayTool.createPayForm(params)
	#将payhtml写到页面，这是个包含有提交按钮的表单
	
	
	#flash('Your orders have been submited~~')
	return render_template("list.html",payhtml=payhtml,row=row,price=price,total_fee=total_fee)
	
@app.route('/nopay',methods=['POST'])
def nopay():
	f=request.form
	g.db.execute('update orders set re=1 where id=?',[f['out_trade_no']])
	g.db.commit()
	money=g.db.execute('select sum(price*numbers) from orders where pay=0 and re=1 and tel=?',[session['phone']]).fetchall()[0][0]
	if money:
		session['money']=float(money)
	else:
		session['money']=0
	g.db.execute('update users set money=? where tel=?',[float(money),session['phone']])
	g.db.commit()
	return render_template("later.html")
	

@app.route('/test',methods=['POST'])
def test():
	f=request.form
	rlt=alipayTool.notifiyCall(f,verify=True)
	if rlt=='success':
		g.db.execute('update orders set re=1 and pay=1 where tel=?',[f['receive_mobile']])
		#g.db.execute('update users set score=score+? where tel=?',[int(float(f['total_fee'])*10),f['receive_mobile']])
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
	file.save(PATH+'static/1_fruit_sum_time.xls')
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
	file.save(PATH+'static/2_user_position_fruit.xls')
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
	file.save(PATH+'static/3_campus_fruit_sum_time.xls')
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
	file.save(PATH+'static/4_fruit_summoney.xls')
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
	file.save(PATH+'static/5_user_money.xls')
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
	file.save(PATH+'static/6_user.xls')
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
	file.save(PATH+'static/7_user.xls')
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

	
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')
