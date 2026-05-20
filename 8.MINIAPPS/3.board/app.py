from flask import Flask, send_from_directory,request,jsonify
from database import MyDatabase


app = Flask(__name__)
db = MyDatabase()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

#INSERT
@app.route('/create', methods=['POST'])
def create():
    data=request.get_json()
    title=data['title']
    contents=data['contents']

    sql = "INSERT INTO board(title,contents) values(?,?)"
    db.execute(sql, (title, contents))
    db.commit()
    
    return jsonify({'result': 'success'})

#SELECT
@app.route('/list')
def list():
    sql="select * from board"
    result=de.execute_fetch(sql) #읽기만 하니까 fetch
    return jsonify({'result': 'success'})

#DELETE
@app.route('/delete', methods=['POST'])
def delete():
    data=request.get_json()
    id=data['id']

    sql="delete from board where id=?"
    db.execute(sql,(id,))
    db.commit()

    return jsonify({'result': 'success'})

#MODIFY
@app.route('/modify', methods=['POST'])
def modify():
    data=request.get_json()
    id=data['id']
    title=data['title']
    contents=data['contents']

    sql="update board set title=?, contents=? where id=?"
    db.execute(sql,(title,contents,id))
    db.commit()

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(debug=True)