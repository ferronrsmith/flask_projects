/*Image Table*/

drop table if exists image;
create table image
(
  id integer primary key autoincrement,
  filename string not null,
  image blob not null,
  shorturl string not null,
  dateadded string not null,
  ext string not null,
  mimetype string not null
);