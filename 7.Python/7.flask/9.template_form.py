from flask import Flask,render_template
from flask import request
import os

app=Flask(__name__)

#저장소 설정
app.config['UPLOAD_FOLDER']='uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    ALLOW_EXT={'png','jpg','jpeg','gif'}
    

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', methods=['POST'])
def login():
    id=request.form.get('id')
    pw=request.form.get('pw')
    print(f"입력한 ID : {id}, PW : {pw}")

    return render_template('login.html',name=id)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['photo']
    print(file)

    filename=file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath) 
    return "파일 잘 받았음"

if __name__=='__main__':
    app.run(debug=True)