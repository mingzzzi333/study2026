from flask import Flask,render_template,request
app=Flask(__name__)

#사용자 로컬
users=[
    {'name': '홍길동', 'id': 'hong123', 'pw': '1234'},
    {'name': '김철수', 'id': 'kim456', 'pw': 'abcd'},
    {'name': '이영희', 'id': 'lee789', 'pw': 'qwer'}
]

@app.route('/', methods={'GET','POST'})
def home():
    if request.method == 'POST':
        id=request.form['id']
        pw=request.form['pw']
        print(f"입력값:{id},{pw}")

        user=None
        for u in users:
            if u['id'] == id and u['pw']==pw:
                user = u
        if user:
            error=None
        else:
            error = "invalid ID or Pw"

        return render_template('index.html',user=user,error=error)

    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)