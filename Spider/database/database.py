import sqlite3

conn = sqlite3.connect("./database.db", check_same_thread=False)

conn.execute(
    "create table if not exists meta (id integer primary key autoincrement not null, `url` varchar(255) not null, title varchar(255) not null, description varchar(255) not null );"
)
conn.commit()
