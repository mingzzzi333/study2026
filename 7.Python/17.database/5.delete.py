import sqlite3

#db연결
conn=sqlite3.connect('example.db')

#커서라는 객체를 통해서, 실제 데이터 입출력을 함.
cur=conn.cursor()


#테이블 생성
cur.execute("""
        update users set age=28 where name ='Bob'
            """)


conn.commit()
conn.close()