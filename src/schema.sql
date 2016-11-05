drop table if exists contacts;
create table contacts (
    id integer primary key autoincrement,
    name text unique not null,
    fingerprint text	
);

drop table if exists settings;
create table settings (
    name text unique not null,
    value text
);
