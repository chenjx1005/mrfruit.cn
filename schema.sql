CREATE TABLE fruits(
f_id integer primary key autoincrement,
f_name text not null,
price real not null, price2, tip, sale);
CREATE TABLE msg(
id integer primary key autoincrement,
tel text not null,
time text not null,
me text not null,
time2 text,
fruit text);
CREATE TABLE orders(
id text not null,
tel text not null,
f_id integer not null,
numbers integer not null,
weekday integer not null,
time text not null,
re integer not null, f_name, price, pay integer, buytime text);
CREATE TABLE receive(id text not null);
CREATE TABLE users(tel text primary key not null,id text not null,name text not null,mail text not null,money real,campus text,building text,room text,score integer, news default 0);


CREATE TABLE receive(id text not null);
delete from fruits;
insert into fruits values(1,"精品香蕉",1.2,3.2,0,0);
insert into fruits values(2,"鸭梨",1.8,4.2,0,0);
insert into fruits values(3,"香梨",1.8,6.2,0,0);
insert into fruits values(4,"大台芒",3.7,8.6,0,0);
insert into fruits values(5,"冰糖心苹果",3.5,7.4,0,0);
insert into fruits values(6,"红富士苹果",1.8,4.5,0,0);
insert into fruits values(7,"猕猴桃",2.6,7.2,0,0);


create table oreal(
f_id integer primary key autoincrement,
f_name text not null,
price real not null, price2,numbers integer,allnum integer);

CREATE TABLE orealorders(
id text not null,
tel text not null,
f_id integer not null,
numbers integer not null,
re integer not null, f_name, price,buytime text);

insert into oreal values(1,"巴黎欧莱雅肌底透白滋润洁面乳 100ml",20,35,300,300);
insert into oreal values(2,"巴黎欧莱雅肌底透白深透精华水 150ml",60,89,300,300);
insert into oreal values(3,"巴黎欧莱雅肌底水润多重保湿霜（清润型）50ml",55,89,200,200);
insert into oreal values(4,"巴黎欧莱雅清润全日保湿水精华凝露（新包装）50ml",80,140,200);
insert into oreal values(5,"巴黎欧莱雅雪颜微震按摩亮白眼霜 15ml",110,220,200,200);
insert into oreal values(6,"巴黎欧莱雅BB隔离露SPF30+/PA+++ 30ml",65,150,300,300);
insert into oreal values(7,"巴黎欧莱雅青春密码 活颜精华肌底液30ml",180,280,200,200);
insert into oreal values(8,"巴黎欧莱雅金致臻颜奢养紧妍日霜50ml",140,280,100,100);
insert into oreal values(9,"巴黎欧莱雅金致臻颜奢养紧妍眼霜15ml",180,280,200,200);
insert into oreal values(10,"巴黎欧莱雅美眸深邃眼线水笔 黑色 1.6g",50,90,100,100);
insert into oreal values(11,"巴黎欧莱雅飞翘胶原睫毛膏 11ml",70,150,200,200);
insert into oreal values(12,"巴黎欧莱雅魅力炫彩持久唇蜜甜心小姐-覆盆子707 6ml",55,100,150,150);
insert into oreal values(13,"巴黎欧莱雅欧莱雅奇焕光感三色焕亮美白粉饼 N1 7.5g",110,230,150,150);
insert into oreal values(14,"巴黎欧莱雅唇部及眼部卸妆液 150ml",55,100,150,150);
insert into oreal values(15,"巴黎欧莱雅男士控油炭爽净亮洁面膏 100ml",20,39,300,300);
insert into oreal values(16,"巴黎欧莱雅男士劲能醒肤露8重功效 50ml",50,100,300,300);
insert into oreal values(17,"美宝莲精纯矿物奇妙新颜乳霜 30ml",40,99,300,300);
insert into oreal values(18,"美宝莲宝蓓粉嫩光采蜜乳 SPF26 PA++ 30ml",35,79,300,300);
insert into oreal values(19,"美宝莲持久魅影眼线膏-黑色 3G",40,89,150,150);
insert into oreal values(20,"美宝莲飞箭睫毛膏 10ml",50,99,150,150);
insert into oreal values(21,"美宝莲睛采造型四色眼影 璀璨钻石系列01 2.5G",30,79,50,50);
insert into oreal values(22,"美宝莲轻裸色系绝色持久唇膏 NE04  3.9g",40,89,150,150);
insert into oreal values(23,"美宝莲水晶胶原唇彩 CP21  7ML",30,69,150,150);
insert into oreal values(24,"美宝莲奇妙净颜 焕白洁面膏100ml",15,49,150,150);
insert into oreal values(25,"美宝莲奇妙净颜 盈润卸妆油120ml",50,99,100,100);
insert into oreal values(26,"薇姿净颜无瑕祛痘保湿柔肤水 200ml",95,175,100,100);
insert into oreal values(27,"薇姿净颜无瑕祛痘保湿霜 50ml",120,200,200,200);
insert into oreal values(28,"理肤泉清痘净肤细致焕颜乳30ml",120,215,200,200);
insert into oreal values(29,"理肤泉立润密集保湿霜（清爽型）50ml",135,235,100,100);


