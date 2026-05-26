import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'board.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

# Initialize DB on start
init_db()

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT id, title, message, created_at FROM posts ORDER BY created_at DESC')
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def add_post():
    title = request.form.get('title', '').strip()
    message = request.form.get('message', '').strip()
    
    if title and message:
        db = get_db()
        db.execute('INSERT INTO posts (title, message) VALUES (?, ?)', (title, message))
        db.commit()
        
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
