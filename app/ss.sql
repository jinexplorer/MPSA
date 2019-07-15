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
	 phone_number varchar(11) NOT NULL,
     primary key(team_name,phone_number)
)engine=InnoDB default charset=utf8;