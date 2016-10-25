drop table if exists contacts;

create table contacts(
	id	integer primary key autoincrement,
	name	text				not null,
	key 	text				not null
	);

insert into contacts(name, key) values ( 'kkkk', 'vnakndlaublievabul' );

