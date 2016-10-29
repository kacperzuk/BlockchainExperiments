drop table if exists contacts;

create table contacts(
	id	integer primary key autoincrement,
	name	text				not null,
	fingerprint 	text	
	);

insert into contacts(name) values ('ania');
insert into contacts(name) values ('adam');
