import sqlite3

#db연결
conn=sqlite3.connect('example.db')

#커서라는 객체를 통해서, 실제 데이터 입출력을 함.
cur=conn.cursor()


#테이블 생성
cur.execute("""
    create table users(
            id integer primary key,
            name text not null,
            age integer not null
            )
            """)

conn.commit()
conn.close()