create table if not exists board(
    id integer primary key autoincrement,
    title text not null,
    contents text not null,
    created_at timestamp default current_timestamp
);
<--IF NOT EXISTS : app.py실행할 때마다 테이블 없으면 만들고, 있으면 넘어감-->
CREATE TABLE IF NOT EXISTS users ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

