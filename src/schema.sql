drop table if exists contacts;

create table contacts (
    id integer primary key autoincrement,
    name text unique not null,
    fingerprint text	
);
