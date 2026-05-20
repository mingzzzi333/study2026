from flask import Flask,render_template,request
from flask import redirect,url_for
from flask import session,flash

from datetime import timedelta

import sqlite3

app=Flask(__name__)
app.secret_key='hello1234'

app.parmanenr_session_lifetime=timedelta(minutes=5)

DATABASE='users.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        cur=conn.cursor()
        cur.execute('''
                    create table if not exists users(
                    id integer primary kwy autoincrement,
                    username tw=ext not null,
                    password twxt not null)
                    ''')
        cur.execute("select count(*)as count from users")
        count=cur.fetchone()['count']
        if count == 0:
            cur.execute("insert into users(username,password) value(?,?)",("user1","password"))
            cur.execute("insert into users(username,password) value(?,?)",("user1","password"))
            

@app.route('/')
def home():
    return render_template('index.html') 
@app.route('login')
def login():
    return "이따 구현" 
@app.route('/')
def logout():
    return "이따가 구현" 
