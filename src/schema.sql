-- drop old tables
drop table if exists contacts;
drop table if exists settings;
drop table if exists conversation;
drop table if exists message;

-- create table for conversations
create table conversation (
    id integer primary key autoincrement,
    name text not null,
    last_message_time text null,
    message_count integer default 0,
    our_next_fingerprint text not null,
    their_next_fingerprint text null
);

create table message (
    id integer primary key autoincrement,
    conversation_id integer not null,
    content text,
    incoming integer not null default '0',
    datetime text
);
