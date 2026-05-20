import sqlite3

class MyDatabase():
    def __init__(self):
        self.db = sqlite3.connect('board.sqlite', check_same_thread=False)
        self.cursor = self.db.cursor()

    def create_table(self):
        with open('init_database.sql','r') as f:
            sql=f.read()

    def execute(self, query, args={}): #결과 필요없는 쿼리 (Insert,Update,Delete)
        self.cursor.execute(query, args)

    def execute_fetch(self, query, args={}): #결과 필요한 쿼리 (Select)
        self.cursor.execute(query, args)
        result = self.cursor.fetchall()
        return result
    
    def commit(self): #이건 필수 안되면 DB저장 안됨.
        self.db.commit()