import sqlite3
import os

absolute_path = os.path.dirname(__file__)
relative_path = "./database.db"
full_path = os.path.join(absolute_path, relative_path)

conn = sqlite3.connect(full_path, check_same_thread=False)

conn.execute(
    "create table if not exists meta (id integer primary key autoincrement not null, `url` varchar(255) not null, title varchar(255) not null, description varchar(255) not null );"
)
conn.execute(
    "create table if not exists titles (id integer primary key autoincrement not null, meta_id integer not null, title varchar(255) not null);"
)
conn.commit()
