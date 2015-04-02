/*Registration/Login Table*/

drop table if exists register;
create table register(
  rid integer primary key autoincrement,
  username string not null,
  fname string not null,
  lname string not null,
  pwd string not null
);

/*Url Table*/

drop table if exists url;
create table url(
  id integer primary key autoincrement,
  longurl string not null,
  shorturl string not null,
  rid integer not null,
  FOREIGN KEY (rid) REFERENCES register(rid)
);