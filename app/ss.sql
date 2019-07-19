create table manage_user(
     phone_number varchar(11) NOT NULL,
     password varchar(32) NOT NULL,
     primary key(phone_number)
)engine=InnoDB default charset=utf8;

create table common_user(
     phone_number varchar(11) NOT NULL,
     password varchar(32) NOT NULL,
     primary key(phone_number)
)engine=InnoDB default charset=utf8;

create table common_user_information(
     phone_number varchar(11) NOT NULL,
	 student_number varchar(13) NOT NULL,
	 sex varchar(2)  CHECK(sex IN ('男','女')),
	 name varchar(40) NOT NULL,
	 description varchar(100) NOT NULL,
     primary key(phone_number)
)engine=InnoDB default charset=utf8;
create table manage_user_information(
     phone_number varchar(11) NOT NULL,
	 student_number varchar(13) NOT NULL,
	 sex varchar(2)  CHECK(sex IN ('男','女')),
	 name varchar(40) NOT NULL,
	 description varchar(100) NOT NULL,
     primary key(phone_number)
)engine=InnoDB default charset=utf8;
create table team(
     team_name varchar(40) NOT NULL,
     category varchar(32)  NOT NULL,
	 description varchar(500) NOT NULL,
	 create_user varchar(11) NOT NULL,
     primary key(team_name)
)engine=InnoDB default charset=utf8;
create table team_user(
     team_name varchar(40) NOT NULL,
     user_name varchar(40) NOT NULL,
	 phone_number varchar(11) NOT NULL,
     primary key(team_name,phone_number)
)engine=InnoDB default charset=utf8;
create table message(
     team_name varchar(40) NOT NULL,
	 title varchar(40) NOT NULL,
     content varchar(500) NOT NULL,
	 create_time varchar(50) NOT NULL,
     primary key(team_name,title)
)engine=InnoDB default charset=utf8;
create table security_question(
     question varchar(100) NOT NULL,
	 answer varchar(32) NOT NULL,
     phone_number varchar(11) NOT NULL,
     primary key(phone_number)
)engine=InnoDB default charset=utf8;
create table systemnews(
     phone_number varchar(11) NOT NULL,
	 team_name varchar(40) NOT NULL,
     type varchar(500) NOT NULL,
	 status varchar(50) NOT NULL,
	 create_time varchar(50) NOT NULL
)engine=InnoDB default charset=utf8;
insert into common_user(phone_number,password) value ('15927517010','59516c9db92b89346b59e460bedc4cae'),('15827372757','d58e2f077670f4de9cd7963c857f2534');
insert into manage_user(phone_number,password) value ('15927517011','59516c9db92b89346b59e460bedc4cae'),('15827372758','d58e2f077670f4de9cd7963c857f2534'),('13260661213','86c09978e5d437ea471363219a52cfde'),('15527481449','11cf6d9b2bd719127ef8b515b9135e88'),('13898851835','05a179041f6a49791ec3bdd93c0745e1');
insert into common_user_information(phone_number,student_number,sex,name,description) value ('15927517010','2017301500196','男','刘进','这个人很懒'),('15827372757','2017301510011','男','田珩之','这个人也很懒');
insert into manage_user_information(phone_number,student_number,sex,name,description) value ('15927517011','2017301500196','男','刘进','狗管理'),('15827372758','2017301510011','男','田珩之','可以可以'),('13260661213','xxxxxxxxxxxxx','男','陈杰','这个人也很懒'),('15527481449','xxxxxxxxxxxxx','女','朱蓓佳','这个人也很懒'),('13898851835','xxxxxxxxxxxxx','男','张宇光','这个人也很懒');


