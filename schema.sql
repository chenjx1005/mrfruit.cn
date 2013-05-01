create table users(
tel text primary key not null,
id text not null,
name text not null,
mail text not null,
money real,
name1 text,
campus1 text,
building1 text,
room1 text,
campus text,
building text,
room text,
score integer
);

create table orders(
tel text not null, 
f_id integer not null,
numbers integer not null,
weekday integer not null,
time text not null,
re integer not null);

create table fruits(
f_id integer primary key autoincrement,
f_name text not null,
price real not null);

create table msg(
id integer primary key autoincrement,
tel text not null,
time text not null,
me text not null,
time2 text,
fruit text);

CREATE TABLE receive(id text not null);

insert into fruits(f_name,price) values("冰糖心苹果",2);
insert into fruits(f_name,price) values("红富士苹果",1.7);
insert into fruits(f_name,price) values("贡梨",1.5);
insert into fruits(f_name,price) values("香梨",1.2);
insert into fruits(f_name,price) values("桔子",0.3);
insert into fruits(f_name,price) values("香蕉",0.8);
insert into fruits(f_name,price) values("柚子",13);
insert into fruits(f_name,price) values("脐橙",1.7);
insert into fruits(f_name,price) values("麒麟瓜（小）",16);
insert into fruits(f_name,price) values("火龙果",4.2);

